import datetime
import os
import random
import time

from selenium.webdriver.common.by import By
from seleniumbase import Driver

from src.utils import append_crawled_urls, load_crawled_urls

# Dcard URL for "送養" topic
ADOPTION_TAG_URL = "https://www.dcard.tw/topics/%E9%80%81%E9%A4%8A"
RES_SAVE_PATH = "./static/dcard_urls.csv"


def cawling_dcard_urls(target_url_num: int = 30) -> list[tuple[str, str, bool]] | None:
    """
    Crawls the urls in Dcard for posts related to pet adoption.

    Args:
        target_url_num (int): The number of URLs to retrieve. Default is 3.

    Returns:
        list[tuple[str, str]] | None: A list of tuples containing the title and URL of each post.
                                      Returns None if an error occurs.
    """
    target_url = ADOPTION_TAG_URL

    # Load existing URLs to avoid duplicates
    existing_df = load_crawled_urls(RES_SAVE_PATH)
    existing_urls = set(existing_df["url"].tolist()) if not existing_df.empty else set()

    try:
        driver = Driver(uc=True, headless=True)
        driver.uc_open_with_reconnect(target_url, reconnect_time=3, uc_subprocess=False)
        article_section = driver.find_element(
            "xpath", '//*[@id="__next"]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div'
        )
    except Exception as e:
        driver.save_screenshot(
            f"dcard_urls_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png"
        )
        raise RuntimeError(f"Error initializing Chrome driver: {e}") from e

    get_url_num = 0
    scroll_height = 0
    url_result = []
    current_session_urls = set()  # Track URLs found in current session

    while get_url_num < target_url_num:
        try:
            # Scroll down to load more posts
            driver.execute_script(f"window.scrollTo(0, {scroll_height});")
            time.sleep(2)  # Wait for new posts to load

            # Find all post elements
            post_elements = article_section.find_elements(
                By.CLASS_NAME,
                "d_d8_1hcvtr6.d_cn_2h.d_gk_10yn01e.d_7v_gdpa86.d_1938jqx_2k.d_2zt8x3_1y.d_grwvqw_gknzbh.d_1ymp90q_1s.d_89ifzh_1s.d_1hh4tvs_1r.d_1054lsl_1r.t1gihpsa",
            )

            for ele in post_elements:
                post_url = ele.get_attribute("href")
                title = ele.text

                # Check if URL already exists in file or current session
                if (
                    post_url not in existing_urls
                    and post_url not in current_session_urls
                ):
                    url_result.append((title, post_url, False))
                    current_session_urls.add(post_url)
                    get_url_num += 1
                    print(f"Added new URL: {post_url}")
                elif post_url in existing_urls:
                    print(f"URL already exists in file: {post_url}")
                else:
                    print(f"Duplicate URL found in current session: {post_url}")

                if get_url_num >= target_url_num:
                    break

            if get_url_num >= target_url_num:
                break
        except Exception as e:
            raise RuntimeError(f"Error retrieving post elements: {e}") from e
        finally:
            driver.quit()

        scroll_height += random.randint(300, 600)

    print(f"Retrieved {len(url_result)} new URLs.")

    return url_result[:target_url_num]


def main():
    """
    Main function to crawl Dcard URLs and save them to a CSV file.
    """
    # Ensure static directory exists
    os.makedirs(os.path.dirname(RES_SAVE_PATH), exist_ok=True)
    
    target_urls = cawling_dcard_urls()
    if target_urls:
        print("Crawled URLs:")
        for title, url, crawled_content in target_urls:
            print(f"Title: {title}, URL: {url}, Crawled Content: {crawled_content}")
    else:
        print("No URLs found.")

    # Save the crawled URLs to a CSV file
    append_crawled_urls(RES_SAVE_PATH, target_urls)


if __name__ == "__main__":
    main()
