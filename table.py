import textwrap

def show_results(data):
    headers = ["ID", "Title", "Year", "Genre", "Actors", "Price", "Description"]
    widths = [5, 20, 7, 12, 30, 8, 38]  # ширина колонок

    # заголовок
    header_line = ""
    for h, w in zip(headers, widths):
        header_line += h.ljust(w) + " "
    print(header_line)
    print("-" * len(header_line))

    # колонки с переносами, где надо
    for row in data:
        # разбиваю каждую ячейку на строки с переносом
        wrapped_cols = [
            textwrap.wrap(str(row[i]), width=w) or [''] for i, w in enumerate(widths)
        ]

        # максимальное число строк в этом ряду (для переносов)
        max_lines = max(len(col) for col in wrapped_cols)

        # по строкам, чтобы переносить текст в ячейках
        for i in range(max_lines):
            line = ""
            for col, w in zip(wrapped_cols, widths):
                # если в этом столбце есть строка на текущей линии, печатаем или пробелы
                cell = col[i] if i < len(col) else ''
                line += cell.ljust(w) + " "
            print(line)


def print_top_searches(data):
    print("Most frequent search queries:")
    for i, item in enumerate(data, start=1):
        print(f"{i}. {item['_id']} — {item['count']} times")

    