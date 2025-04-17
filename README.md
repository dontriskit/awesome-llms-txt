# llms.txt Guide

This repository demonstrates how to extract and store `llms.txt` files from websites and provides a template for creating your own `llms.txt` to help Large Language Models (LLMs) interact with your site.

## What is llms.txt?

`llms.txt` is a lightweight, plain-text standard (inspired by `robots.txt`) for websites to expose relevant endpoints, documentation, and content pointers to LLMs. At inference time, LLM-powered agents and crawlers can fetch this file to guide their retrieval or browsing behavior.

## Creating Your llms.txt

1. **Host at root**: Place a `llms.txt` file at the root of your domain:
   ```
   https://your-domain.com/llms.txt
   ```

2. **Use plain text or simple key-value pairs**. Include:
   - **Title:** Your project or site name
   - **Description:** A short summary of your site’s purpose
   - **Links:** A list of URLs (docs, API endpoints, tutorials, blog posts) for deeper fetches
   - **Category:** (Optional) Keywords or categories describing your content

3. **Example format**:
   ```text
   Title: MyProject
   Description: A platform for AI-powered analytics.
   Category: Analytics, AI

   Links:
     - https://your-domain.com/docs/api/overview
     - https://your-domain.com/tutorials/llm-usage
     - https://your-domain.com/blog/releases
   ```

4. **Optional `llms-full.txt`**: If you need to expose larger content (full docs or extended guides), host an optional file:
   ```
   https://your-domain.com/llms-full.txt
   ```
   This file can contain complete documentation or aggregated content.

## Testing & Validation

Use the provided scraper to verify correct hosting:

```bash
pip install playwright aiohttp aiofiles
playwright install
python3 scraper.py
```

Your `llms.txt` (and `llms-full.txt`, if present) will be fetched, saved under `awesome-llms-txt/<your_domain>/`, and indexed in `_metadata.json`.

## Best Practices

- Keep `llms.txt` concise (<50 KB).
- Use absolute URLs for clarity.
- Organize links into sections for readability.
- Update regularly to reflect site changes.
- Test under different user-agent headers.

## Contributing

Contributions and improvements are welcome! Please open issues or PRs to add your site or refine this guide.

## License

[MIT](LICENSE)
