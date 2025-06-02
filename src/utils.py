import pandas as pd


def load_crawled_urls(RES_SAVE_PATH) -> pd.DataFrame:
    """
    Loads previously crawled Dcard URLs from a CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the crawled URLs and their titles.
    """
    try:
        df = pd.read_csv(RES_SAVE_PATH)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["id", "title", "url", "crawled_content"])


def append_crawled_urls(RES_SAVE_PATH, urls: list[tuple[int, str, str, bool]]) -> None:
    """
    Appends new crawled URLs to the existing CSV file.

    Args:
        urls (list[tuple[str, str, bool]]): A list of tuples containing the title, URL, and a flag indicating if content was crawled.
    """
    df = load_crawled_urls(RES_SAVE_PATH)

    # Get the next ID number (starting from 1 if the DataFrame is empty)
    next_id = 1 if df.empty else df["id"].max() + 1

    new_rows = []
    for title, url, crawled_content in urls:
        new_rows.append(
            {
                "id": next_id,
                "title": title,
                "url": url,
                "crawled_content": crawled_content,
            }
        )
        next_id += 1

    # Use pd.concat instead of deprecated append
    new_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_df], ignore_index=True)

    df.to_csv(RES_SAVE_PATH, index=False)
    print(f"Appended {len(urls)} new URLs to {RES_SAVE_PATH}.")
