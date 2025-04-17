# Awesome llms.txt

A curated collection of `llms.txt` files from across the web. This repository indexes `llms.txt` from over 130 websites, making it easy to discover LLM‑friendly documentation endpoints and tutorials.

## What is llms.txt?

`llms.txt` is a lightweight, plain-text standard (inspired by `robots.txt`) for websites to expose relevant endpoints, documentation, and content pointers to LLMs. At inference time, LLM-powered agents and crawlers can fetch this file to guide their retrieval or browsing behavior.

## Popular LLM Providers

An analysis of the `llms.txt` corpus shows the most referenced providers:

| Provider               | Website Count |
|------------------------|--------------:|
| Google Vertex AI       | 91            |
| Microsoft Azure OpenAI | 36            |
| OpenAI                 | 28            |
| Anthropic              | 16            |
| Cohere                 | 10            |
| AI21 Labs              | 3             |

## Creating Your llms.txt

For a detailed, step-by-step guide on writing your own `llms.txt`, see [Writing Your Own llms.txt](docs/guide.md).

## Getting Started

### Install dependencies

```bash
pip install playwright aiohttp aiofiles
playwright install
```

### Fetch `llms.txt`

```bash
python3 scraper.py
```

Fetched `llms.txt` files will be saved under `websites/<your_domain>/` and indexed in `_metadata.json`.

## Testing & Validation

Use the provided scraper to verify correct hosting.

## Best Practices

- Keep `llms.txt` concise (<50 KB).
- Use absolute URLs for clarity.
- Organize links into sections for readability.
- Update regularly to reflect site changes.
- Test under different user-agent headers.

## Contributing

Contributions are welcome! Please open an issue or PR to:

- Add a new site's `llms.txt`
- Improve the guide in `docs/`
- Refine the analysis or tooling

## License

[MIT](LICENSE)
