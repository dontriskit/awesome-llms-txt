# Writing Your Own llms.txt

This guide walks you through authoring and hosting an `llms.txt` file for your website. LLM-powered agents and crawlers can fetch this file to discover key documentation endpoints, tutorials, and resources.

## 1. Host at the Root

Place your `llms.txt` at the root of your domain so it’s easily found:

```
https://your-domain.com/llms.txt
```

## 2. File Format

Use plain text with simple key-value pairs and sections. Include:

- **Title:** Your project or site name
- **Description:** A concise summary of what your site offers
- **Category:** (Optional) Comma-separated tags to describe content
- **Links:** A list of URLs to docs, APIs, tutorials, or blogs

## 3. Minimal Example

```text
Title: MyProject
Description: A platform for AI-powered analytics
Category: Analytics, AI

Links:
  - https://your-domain.com/docs/api/overview
  - https://your-domain.com/tutorials/llm-usage
  - https://your-domain.com/blog/releases
```

## 4. Optional Full Documentation

If you need to expose larger content (full docs or extended guides), host an optional file:

```
https://your-domain.com/llms-full.txt
```

This file can contain complete reference docs or aggregated tutorials.

## 5. Testing & Validation

Use the provided scraper to verify correct hosting and syntax:

```bash
pip install playwright aiohttp aiofiles
playwright install
python3 scraper.py
```

Successful fetches are saved under `websites/<your_domain>/` and indexed in `_metadata.json`.

## 6. Best Practices

- Keep `llms.txt` concise (under 50 KB)
- Use absolute URLs for clarity
- Organize links into logical sections (e.g., APIs, Tutorials, Blog)
- Update regularly to reflect documentation changes
- Test with different User-Agent headers to ensure accessibility

## 7. Advanced Tips

- Group endpoints by version or functionality
- Add a comment header with a version or date
- Use caching headers to control freshness (e.g., `Cache-Control`)

---

Happy authoring! If you have suggestions, feel free to open an issue or PR.
