
    offset = 0
    while True:
        data = search_func(*args, offset)
        if not data:
            print("No results found.")
            break

        table.show_results(data)  # display results

        if len(data) < settings.MOVIE_RESULT_LIMIT:
            print("End of results.")
            break

        user_input = input("Show next 10 results? Type 'yes' to continue, or '0' to return to the main menu: ").strip().lower()

        if user_input == 'yes':
            offset += settings.MOVIE_RESULT_LIMIT
            continue
        elif user_input == '0':
            print("Returning to the main menu.")
            break
        else:
            print("Invalid input. Returning to the main menu.")
            break