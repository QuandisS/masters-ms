#!/bin/bash

read -p "Введите число: " number

if [[ $number -gt 0 ]]; then
    echo "Число положительное."
    count=1
    while [[ $count -le $number ]]; do
        echo $count
        ((count++))
    done

elif [[ $number -lt 0 ]]; then
    echo "Число отрицательное."
else
    echo "Вы ввели ноль."
fi
