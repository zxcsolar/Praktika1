# Эмулятор командной оболочки UNIX-подобной ОС.

## Запуск
```bat
run.bat demo-vfs
```
или

```bat
python src\console.py --vfs demo-vfs
```

## Реализованные команды:
- ls — команда-заглушка
- cd — команда-заглушка
- exit — завершение работы

Поддерживается раскрытие переменных окружения, например:
```text
ls $HOME
```
## Параметры командной строки

Поддерживаются параметры:

- `--vfs` — имя или путь к VFS
- `--startup` — путь к стартовому скрипту
- `--config` — путь к конфигурационному файлу

Пример:

```bat
python src\console.py --vfs demo-vfs --startup startup.txt --config config.ini
```

## Конфигурационный файл

Файл `config.ini` имеет формат:

```ini
[emulator]
vfs = config-vfs
startup = startup.txt
```

## Стартовый скрипт

Стартовый скрипт содержит команды эмулятора, которые выполняются при запуске.

Пример:

```text
ls
cd /home
ls $HOME
```

## Тестовые скрипты

Для проверки параметров запуска используются:

- `test_vfs.bat`
- `test_startup.bat`
- `test_config.bat`
- `test_priority.bat`