package com.example.study.ex07

import java.io.BufferedReader
import java.io.File
import java.io.FileReader
import java.io.IOException

fun main() {
    try {
        readFile()
    } catch (e: IOException) {
        println("e: ${e.message}")
    }
}

fun readFile() {
    val currentFile = File(".");
    val file = File(currentFile.absolutePath + "/README2.md");
    // use 블록으로 예외 발생 여부와 무관하게 자동 close
    BufferedReader(FileReader(file)).use { reader ->
        println(reader.readLine());
    }
}

@Throws(IOException::class)
fun readFile(path: String) {
    BufferedReader(FileReader(path)).use { reader ->
        println(reader.readLine())
    }
}