# First Dollar

A self-contained, practical guide to investing in the United States through ETFs and other US-domiciled options.

## Publish with GitHub Pages

1. Create an empty GitHub repository.
2. Add it as this repository's `origin` and push the `main` branch.
3. In the GitHub repository, open **Settings → Pages**.
4. Under **Build and deployment**, select **GitHub Actions** as the source.
5. Open the repository's **Actions** tab and wait for **Deploy GitHub Pages** to finish.

The workflow publishes the contents of `outputs/`. The public entry point is `outputs/index.html`.

## Rebuild after editing

Edit the chapter, style, or script files under `work/`, then run:

```sh
python3 work/build.py
```

Commit both generated HTML files after rebuilding. The site has no package dependencies or external asset build step.
