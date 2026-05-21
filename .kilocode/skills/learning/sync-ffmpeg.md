# Sync FFmpeg Learnings
## AAC Packet Padding Can Extend Post-Mux Containers
<!-- meta: date=2026-05-20, tier=2, status=active -->
- **Trigger/Symptom**: Post-mux container duration follows rendered audio and exceeds video by one to three AAC packets.
- **Cause/Mistake**: AAC muxing preserves 1024-sample packet boundaries, so packet padding can make the container report the longer audio duration.
- **Fix/Correct**: Use output-side `-t <video_duration>` immediately before the output path in `io_/video_renderer_twophase.py` so the muxed container is capped to the rendered video stream.
- **Verification**: Compare pre-mux and post-mux `[SYNC-DEBUG]` runtime log lines captured by `utils/progress_log.py`; video duration should stay authoritative after mux.
- **Why**: `atrim` and `-shortest` are useful defenses, but they do not always remove AAC packet-padding drift at container finalization.
