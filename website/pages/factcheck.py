import requests

def get_latest_fact_checks(search_term):
    api_key = 'AIzaSyB9BgMqW9AXGQD0ZfHWgFrtq6tTz9WEUVo'  # Replace with your actual API key

    # API endpoint URL
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?key={api_key}"

    # Request parameters
    params = {
        'query': search_term,
        'pageSize': 10,  # Number of fact checks to retrieve
        'languageCode': 'en',  # Language code (e.g., en for English)
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract and print the latest fact checks
        fact_checks = data.get('claims', [])
        for fact_check in fact_checks:
            claim = fact_check.get('claim', '')
            claimant = fact_check.get('claimant', '')
            rating = fact_check.get('textualRating', '')
            claim_date = fact_check.get('claimDate', '')
            review = fact_check.get('claimReview', [])

            print(f"Claim: {claim}")
            print(f"Claimant: {claimant}")
            print(f"Rating: {rating}")
            print(f"Claim Date: {claim_date}")

            if review:
                for item in review:
                    publisher_name = item['publisher'].get('name', '')
                    publisher_site = item['publisher'].get('site', '')
                    review_url = item.get('url', '')
                    review_title = item.get('title', '')
                    review_date = item.get('reviewDate', '')
                    textual_rating = item.get('textualRating', '')
                    language_code = item.get('languageCode', '')

                    print(f"\nReview by: {publisher_name}")
                    print(f"Publisher Site: {publisher_site}")
                    print(f"Review URL: {review_url}")
                    print(f"Review Title: {review_title}")
                    print(f"Review Date: {review_date}")
                    print(f"Textual Rating: {textual_rating}")
                    print(f"Language Code: {language_code}\n")
            else:
                print("No reviews available for this claim.\n")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {str(e)}")


# Usage example
search_term = 'wrestler protest'
get_latest_fact_checks(search_term)
