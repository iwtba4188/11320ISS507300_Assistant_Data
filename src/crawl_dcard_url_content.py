import datetime
import json
import os
import random
import time
from collections import defaultdict

from seleniumbase import Driver

from src.utils import load_crawled_urls


def crawling_dcard_article_content(target_url: str) -> dict | None:
    """
    Crawls the content of a specific Dcard post.

    Args:
        target_url (str): The URL of the Dcard post to crawl.

    Returns:
        dict | None: A dictionary containing the post's title, author, creation date,
                        and content. Returns None if an error occurs.
    """
    driver = None
    try:
        driver = Driver(uc=True, headless=True)
        driver.uc_open_with_reconnect(target_url, reconnect_time=3)

        result = defaultdict(str)
        result["url"] = target_url

        result["title"] = driver.find_element("tag name", "h1").text
        result["author"] = driver.find_element(
            "class name", "d_xa_2b.d_tx_2c.d_lc_1u.d_7v_5.a6buno9"
        ).text
        result["createdAt"] = driver.find_element("tag name", "time").get_attribute(
            "datetime"
        )

        content_element = driver.find_element("class name", "d_xa_34.d_xj_2v.c1ehvwc9")
        result["content"] = content_element.text

        return result

    except Exception as e:
        if driver:
            driver.save_screenshot(
                f"dcard_content_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            )
        print(f"Error crawling content from {target_url}: {e}")
        return None
    finally:
        if driver:
            driver.quit()


def main():
    """
    Main function to crawl content for all URLs with crawled_content=False
    """
    # Path to the CSV file
    RES_SAVE_PATH = "./static/dcard_urls.csv"

    # Ensure static directory exists
    os.makedirs(os.path.dirname(RES_SAVE_PATH), exist_ok=True)

    # Load existing URLs
    df = load_crawled_urls(RES_SAVE_PATH)

    if df.empty:
        print("No URLs found in the CSV file.")
        return

    # Filter URLs that haven't been crawled yet
    uncrawled_urls = df[~df["crawled_content"]]

    if uncrawled_urls.empty:
        print("All URLs have already been crawled.")
        return

    print(f"Found {len(uncrawled_urls)} URLs to crawl.")

    # Create a new DataFrame to store content
    content_data = []

    for _, row in uncrawled_urls.iterrows():
        url = row["url"]
        print(f"Crawling content from: {url}")

        # Crawl the content
        content = crawling_dcard_article_content(url)

        if content:
            content_data.append(
                {
                    "id": row["id"],
                    "url": url,
                    "title": content["title"],
                    "author": content["author"],
                    "createdAt": content["createdAt"],
                    "content": content["content"],
                }
            )

            # Update the crawled_content status to True
            df.loc[df["id"] == row["id"], "crawled_content"] = True

            print(f"Successfully crawled content for ID {row['id']}")
        else:
            print(f"Failed to crawl content for ID {row['id']}")

        # Add random delay to avoid being blocked
        time.sleep(
            random.uniform(2, 5)
        )  # Save the updated CSV with crawled_content status
    df.to_csv(RES_SAVE_PATH, index=False)
    print(f"Updated crawled_content status in {RES_SAVE_PATH}")

    # Save the crawled content to JSON file (merge with existing content)
    if content_data:
        content_filename = "./static/dcard_contents.json"

        # Load existing content if file exists
        existing_content = []
        try:
            with open(content_filename, "r", encoding="utf-8") as f:
                existing_content = json.load(f)
        except FileNotFoundError:
            print(
                f"No existing content file found. Creating new file: {content_filename}"
            )
        except json.JSONDecodeError:
            print(
                f"Warning: Existing file {content_filename} contains invalid JSON. Starting fresh."
            )

        # Merge new content with existing content
        all_content = existing_content + content_data

        # Save merged content back to JSON file
        with open(content_filename, "w", encoding="utf-8") as f:
            json.dump(all_content, f, ensure_ascii=False, indent=2)
        print(
            f"Merged {len(content_data)} new contents with {len(existing_content)} existing contents in {content_filename}"
        )
        print(f"Total contents now: {len(all_content)}")
    else:
        print("No content was successfully crawled.")


if __name__ == "__main__":
    main()
