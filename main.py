import db
import ui
import mongo_log
import table



def main():
    movie_db = db.MovieDB()

    while True:
        choice = ui.show_menu()

        if choice == 1:  # Поиск фильма
            movie_choice = ui.show_menu_movies()

            if movie_choice == 1:
                name = ui.film_name()
                ui.paginate_query(movie_db.search_film_by_name, name)

            elif movie_choice == 2:
                name = ui.actor_name()
                ui.paginate_query(movie_db.search_film_by_actor, name)

            elif movie_choice == 3:
                desc = ui.description_text()
                ui.paginate_query(movie_db.search_film_by_description, desc)

            elif movie_choice == 4:
                genres = movie_db.query_all_genres()
                print("Available genres:")
                for g in genres:
                    print(f" - {g}")

                year_min, year_max = movie_db.query_min_max_year()
                print(f"Available release years: from {year_min} to {year_max}")

                genre_input = ui.genre_name() #убрать регистрозависимость
                while genre_input not in genres:
                    print("Invalid genre. Please choose from the list.")
                    genre_input = ui.genre_name()
                genre = genres[genre_input]

                while True:
                    min_year = ui.min_year()
                    max_year = ui.max_year()
                    if min_year < year_min or max_year > year_max or min_year > max_year:
                        print(f"Please enter valid years between {year_min} and {year_max}, and min_year <= max_year")
                    else:
                        break

                ui.paginate_query(movie_db.search_film_by_genre_and_year, genre, min_year, max_year)

            elif movie_choice == 0:
                continue

            else:
                print("Invalid choice in the movie menu")

        elif choice == 2:
            top_searches = mongo_log.get_top_5_queries(5)
            table.print_top_searches(top_searches)
            continue

        elif choice == 0:
            print("Exit")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()