#!/bin/bash

echo "Текущее значение PATH: $PATH"

if [ -z "$1" ]; then
  echo "Ошибка: Необходимо указать директорию для добавления в PATH."
  exit 1
fi

export PATH="$1:$PATH"
echo "Новое значение PATH: $PATH"

# Чтобы сделать изменения постоянными, необходимо добавить команду export в файл конфигурации оболочки, 
# например, в ~/.bashrc:
# >> nano ~/.bashrc
# В конец файла добавьте строку для добавления новой директории в PATH:
# export PATH="/ваша/новая/директория:$PATH"
# Сохраните изменения и выйдите из редактора
# Чтобы применить изменения без перезапуска терминала, выполните команду:
# source ~/.bashrc
