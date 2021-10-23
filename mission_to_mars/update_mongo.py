# Examine the results, then determine element that contains sought info
# results are returned as an iterable list
results = soup.find_all('div', class_='caption')

# Loop through returned results
for result in results:
    # Error handling
    try:
        # Identify and return title of listing
        title = result.find('a', class_='title').text
        # Identify and return price of listing
        price = result.find('h4', class_='price').text
        # Identify and return link to listing
        link = result.a['href']
        description = result.find("p", class_="description").text

        # Run only if title, price, and link are available
        if (title and price and link):
            # Print results
            print('-------------')
            print(title)
            print(price)
            print(link)

            # Dictionary to be inserted as a MongoDB document
            post = {
                'title': title,
                'price': price,
                'url': link,
                'description': description
            }

            collection.insert_one(post)

    except Exception as e:
        print(e)