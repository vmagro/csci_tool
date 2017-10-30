package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/spf13/viper"
	"github.com/vmagro/csci_tool/cmd"
)

func main() {
	// flag.Lookup("logtostderr").Value.Set("true")
	flag.Parse()

	viper.SetConfigType("yaml")
	viper.SetConfigName("cscitool") // name of config file (without extension)
	viper.AddConfigPath(".")        // optionally look for config in the working directory

	err := viper.ReadInConfig() // Find and read the config file
	if err != nil {             // Handle errors reading the config file
		panic(fmt.Errorf("fatal error config file: %s", err))
	}

	if err := cmd.RootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
