#!/bin/bash

greet() {
    echo "Hello, $1"
}

sum_numbers() {
    local result=$(( $1 + $2 ))
    echo $result
}

greet "World"

sum_result=$(sum_numbers 10 20)

echo "Сумма чисел 10 и 20 равна: $sum_result"
