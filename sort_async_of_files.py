from rich import print
import asyncio                         # для створення event loop та асинхронних задач.
from pathlib import Path               # для зручної роботи з шляхами.
import shutil                          # для копіювання файлів (у поєднанні з executor).
from argparse import ArgumentParser    # додавання аргументів (шляхів до папок) обробляти помилки при зупуску.
import logging                         # Імпортую стандартний модуль для логування.

# Базове налаштування логування (запис у файл і в консоль)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_arguments():
    parser = ArgumentParser(
        description="Асинхронне сортування файлів по підпапках за розширенням"
    )
    parser.add_argument(
        "source_folder",
        type=str,
        help="Шлях до папки з файлами для сортування"
    )
    parser.add_argument(
        "output_folder",
        type=str,
        help="Шлях до папки, куди розкладати відсортовані файли"
    )
    return parser.parse_args()

async def read_folder(folder: Path) ->list[Path]:
    files = []
    for content in folder.iterdir():
        if content.is_file():
            files.append(content)
        elif content.is_dir():
            subfiles = await read_folder(content)
            files.extend(subfiles)
    return files
    
async def copy_file(file_path: Path, output_folder: Path):
    ext = file_path.suffix.lower().lstrip(".")
    end_dir = output_folder / ext
    end_dir.mkdir(parents = True, exist_ok=True)
    end_file = end_dir/file_path.name

    loop = asyncio.get_running_loop()

    try:
        await loop.run_in_executor(None, shutil.copy2, file_path, end_file)
        logging.info(f"Скопійовано: {file_path} to {end_file}")
    except Exception as e:
        logging.error(f"Помилка копіювання {file_path}: {e}")

async def async_main(source_path: Path, output_path: Path):
    try:
        files = await read_folder(source_path)
    except Exception as e:
        logging.error(f"Відсутні файли в каталозі {source_path}: {e}")
        return

    print(f"[green]Знайдено {len(files)} файлів для копіювання[/green].")

    # Асинхронний запуск копіювання файлів паралельно
    tasks = [copy_file(file_path, output_path) for file_path in files]
    await asyncio.gather(*tasks)

def main():
    args = parse_arguments()
    source_path = Path(args.source_folder)    # тут зберігається шлях до вихідної папки
    output_path = Path(args.output_folder)    # тут зберігається шлях до цільової папки
    # далі ці об'єкти булуть використані у всіх операціях з файлами

    # Перевірю, чи існує source_path
    if not source_path.exists():
        print(f"Вихідна папка {source_path} не існує.")
        raise SystemExit()  #завершує виконання всього скрипта.

    # Якщо output_path не існує — створюю
    output_path.mkdir(parents=True, exist_ok=True)
    # parents=True — створить всі відсутні проміжні папки
    # exist_ok=True — не буде помилки, якщо папка вже існує складники
    
    try:
        files = asyncio.run(async_main(source_path, output_path))
    except Exception as e:
        logging.error(f"Відсутні файли в каталозі {source_path}: {e}")




if __name__ == "__main__":
    main()