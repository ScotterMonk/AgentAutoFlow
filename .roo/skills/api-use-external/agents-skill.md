# External API use

---
THE CONTENTS OF THIS FILE ARE A PLACEHOLDER
The purpose of this file is to provide project specific 
information used by the api-use-external skill.
--
Includes how to query and process the current existing external APIs:
- API 01 placeholder.
- API 02 placeholder.

## API configuration
- All API settings such as keys, base URLs, and timeouts come from `config.py`.
- API credentials and other secrets come from `.env`.

## API provider framework

### API integration

### Base API provider
- `placeholder_file.py` defines `BaseApiProvider` for all external HTTP APIs.
- Handles HTTP requests, authentication, token management, error handling, and response normalization.
- Stateless by design with no Flask context; safe to use in core modules.
- Includes retry strategy and standardized response format.
- Use this class instead of creating custom HTTP client code per API.

### Provider descriptors
- `placeholder_file.py` defines configuration descriptors for each external API.
- New providers should be added by defining a descriptor in this module, not by creating new ad-hoc client modules.
- Descriptors capture base URL, authentication strategy, header builders, and normalization callbacks.
- Supports bearer tokens, API keys, and static tokens.
- Includes `TokenCache` for automatic token refresh and caching where needed.

### Core vs presentation for APIs
- Core API logic belongs in `placeholder_file.py` modules that use BaseApiProvider and descriptors.
- Flask-aware presentation logic belongs in `placeholder_file(s).py` modules that call core functions.
- Keep API core code free of Flask imports and request context.

## Docs and examples
- **API 01 placeholder**: `placeholder_file.md` (IMDb236 API)
- **API 02 placeholder**: `placeholder_file.md` (IMDb8 API) 