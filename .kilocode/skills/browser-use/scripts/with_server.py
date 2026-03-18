#!/usr/bin/env python3
"""
Start one or more servers, wait for them to be ready, run a command, then clean up.

Usage:
    # Single server (port-readiness check)
    python .roo/skills/browser-use/scripts/with_server.py --server "py app.py" --port 5000 -- python automation.py

    # Single server with HTTP health-check URL (more reliable than port probe)
    python .roo/skills/browser-use/scripts/with_server.py --server "py app.py" --port 5000 --health-url http://localhost:5000/healthz -- python automation.py

    # Multiple servers
    python .roo/skills/browser-use/scripts/with_server.py \
      --server "cd backend; python server.py" --port 3000 \
      --server "cd frontend; npm run dev" --port 5173 \
      -- python test.py
"""

import subprocess
import socket
import time
import sys
import argparse
import threading
import urllib.request


def _stream_output(process, label):
    """Read lines from both stdout and stderr and print them with a label prefix.

    Runs in a daemon thread so it never blocks the main thread.
    Draining the pipes prevents the OS pipe buffer from filling up and
    deadlocking the child process when it produces heavy output.
    """
    def _drain(stream, stream_name):
        try:
            for line in stream:
                print(f"[{label}:{stream_name}] {line.rstrip()}", flush=True)
        except Exception:
            pass

    t_out = threading.Thread(target=_drain, args=(process.stdout, 'out'), daemon=True)
    t_err = threading.Thread(target=_drain, args=(process.stderr, 'err'), daemon=True)
    t_out.start()
    t_err.start()


def _port_open(port):
    """Return True if something is accepting connections on localhost:port."""
    try:
        with socket.create_connection(('localhost', port), timeout=1):
            return True
    except (socket.error, ConnectionRefusedError):
        return False


def _http_healthy(url):
    """Return True if the URL returns HTTP 2xx."""
    try:
        with urllib.request.urlopen(url, timeout=2) as resp:
            return 200 <= resp.status < 300
    except Exception:
        return False


def wait_until_ready(process, port, health_url=None, timeout=30, label='server'):
    """Poll until the server is ready or the process dies or the timeout expires.

    Args:
        process: The Popen object for the server.
        port: Port to probe (always checked first).
        health_url: Optional HTTP URL for a deeper health check after port opens.
        timeout: Seconds to wait before raising RuntimeError.
        label: Name used in log messages.

    Returns:
        True on success, raises RuntimeError on failure.
    """
    start = time.time()
    while time.time() - start < timeout:
        # Detect early server exit so we don't wait the full timeout pointlessly
        if process.poll() is not None:
            raise RuntimeError(
                f"[{label}] Process exited early with code {process.returncode} "
                f"before becoming ready on port {port}. "
                f"Check server logs above for details."
            )

        if _port_open(port):
            if health_url:
                # Port is open; also verify the HTTP health endpoint if given
                if _http_healthy(health_url):
                    return True
                # Health endpoint not yet ready — keep polling
            else:
                return True

        time.sleep(0.5)

    raise RuntimeError(
        f"[{label}] Server did not become ready on port {port} within {timeout}s. "
        f"Check server logs above for details."
    )


def main():
    parser = argparse.ArgumentParser(
        description='Run command with one or more servers. '
                    'Server stdout/stderr is streamed to the console in real time.'
    )
    parser.add_argument(
        '--server', action='append', dest='servers', required=True,
        help='Server command (can be repeated for multiple servers)',
    )
    parser.add_argument(
        '--port', action='append', dest='ports', type=int, required=True,
        help='Port for each server (must match --server count)',
    )
    parser.add_argument(
        '--health-url', action='append', dest='health_urls', default=None,
        metavar='URL',
        help=(
            'Optional HTTP health-check URL per server (can be repeated). '
            'When given, the script waits for both the port AND a 2xx response '
            'from this URL before proceeding. '
            'If fewer --health-url values than --server values are given, '
            'remaining servers fall back to port-only check.'
        ),
    )
    parser.add_argument(
        '--timeout', type=int, default=30,
        help='Timeout in seconds per server (default: 30)',
    )
    parser.add_argument(
        'command', nargs=argparse.REMAINDER,
        help='Command to run after all server(s) are ready',
    )

    args = parser.parse_args()

    # Remove the '--' separator if present
    if args.command and args.command[0] == '--':
        args.command = args.command[1:]

    if not args.command:
        print("Error: No command specified to run after --")
        sys.exit(1)

    if len(args.servers) != len(args.ports):
        print("Error: Number of --server and --port arguments must match")
        sys.exit(1)

    # Build health_urls list, padding with None for servers without one
    health_urls = list(args.health_urls or [])
    while len(health_urls) < len(args.servers):
        health_urls.append(None)

    server_configs = [
        {'cmd': cmd, 'port': port, 'health_url': hu}
        for cmd, port, hu in zip(args.servers, args.ports, health_urls)
    ]

    server_processes = []

    try:
        # Start all servers
        for i, server in enumerate(server_configs):
            label = f"server-{i+1}"
            print(f"[{label}] Starting: {server['cmd']}")

            # shell=True supports commands with cd/&&/;
            # text=True gives us str lines for easy printing
            # stdout/stderr are piped so we can drain them in threads
            process = subprocess.Popen(
                server['cmd'],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
            )
            server_processes.append((process, label))

            # Drain pipes in background threads to prevent pipe-buffer deadlock
            _stream_output(process, label)

            # Wait for this server to become ready
            health_hint = f" (health: {server['health_url']})" if server['health_url'] else ""
            print(f"[{label}] Waiting for port {server['port']}{health_hint}...")
            wait_until_ready(
                process,
                port=server['port'],
                health_url=server['health_url'],
                timeout=args.timeout,
                label=label,
            )
            print(f"[{label}] Ready on port {server['port']}")

        print(f"\nAll {len(server_configs)} server(s) ready.")

        # Run the automation command
        print(f"Running: {' '.join(args.command)}\n")
        result = subprocess.run(args.command)
        sys.exit(result.returncode)

    finally:
        # Clean up all server processes
        print(f"\nStopping {len(server_processes)} server(s)...")
        for process, label in server_processes:
            if process.poll() is None:  # Still running
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            print(f"[{label}] Stopped")
        print("All servers stopped.")


if __name__ == '__main__':
    main()
