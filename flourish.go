package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"github.com/DisposaBoy/JsonConfigReader"
)

func find_content(path string, f os.FileInfo, err error) error {
	ext := filepath.Ext(path)
	if ext == ".json" {
		var v interface{}
		json_file, _ := os.Open(path)
		reader := JsonConfigReader.New(json_file)
		json.NewDecoder(reader).Decode(&v)
		fmt.Printf("%s\n", path)
		fmt.Println(v)
	}
	return nil
}


func main() {
	filepath.Walk("content", find_content)
}
