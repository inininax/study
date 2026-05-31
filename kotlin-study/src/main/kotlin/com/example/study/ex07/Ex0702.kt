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
    val reader = BufferedReader(FileReader(file));
    println(reader.readLine());
    reader.close();
}

@Throws(IOException::class)
fun readFile(path: String) {
    BufferedReader(FileReader(path)).use { reader ->
        println(reader.readLine())
    }
}