#!/bin/bash

echo "Список файлов и каталогов в текущей директории:"
file_list=$(file *)
for file in $file_list; do
    echo $file
done

echo

if [ $# -gt 0 ]; then
    file_to_check="$1"
    if [ -e "$file_to_check" ]; then
        echo "Файл '$file_to_check' существует."
    else
        echo "Файл '$file_to_check' не найден."
    fi
fi

echo 
echo "Информация о файлах и их правах доступа:"
for file in *; do
    if [ -e "$file" ]; then
        permissions=$(ls -l "$file" | awk '{print $1}')
        echo "$file: $permissions"
    fi
done
