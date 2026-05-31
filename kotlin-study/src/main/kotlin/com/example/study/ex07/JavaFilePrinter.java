package com.example.study.ex07;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class JavaFilePrinter {
    public static void main(String[] args) throws IOException {
        new JavaFilePrinter().readFile();
    }

    public void readFile() throws IOException {
        File currentFile = new File(".");
        File file = new File(currentFile.getAbsoluteFile() + "/README.md");
        BufferedReader reader = new BufferedReader(new FileReader(file));
        System.out.println(reader.readLine());
        reader.close();
    }

    public void readFile(String path) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            System.out.println(reader.readLine());
        }
    }
}
