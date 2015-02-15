package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func find_content(path string, f os.FileInfo, err error) error {
	ext := filepath.Ext(path)
	if ext == ".json" {
		fmt.Printf("%s\n", path)
	}
	return nil
}


func main() {
	filepath.Walk("content", find_content)
}
