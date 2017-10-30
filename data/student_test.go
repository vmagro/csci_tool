package data

import (
	"testing"

	"github.com/spf13/viper"
)

func TestRepoName(t *testing.T) {
	s := Student{
		UnixName:      "smagro",
		UscID:         "12345",
		PreferredName: "Vinnie",
		Github:        "vmagro",
		FirstName:     "Stephen",
		LastName:      "Magro",
	}
	viper.Set("RepoNameTemplate", "hw_{{.UnixName}}")
	defer viper.Reset()
	repoName, err := s.RepoName()
	if err != nil {
		t.Fatalf("Failed to get RepoName: %s", err)
	}
	if repoName != "hw_smagro" {
		t.Fatalf("Expected repo name to be hw_smagro, got %s", repoName)
	}

	// make sure it also works with a custom template
	viper.Set("RepoNameTemplate", "hw_{{.PreferredName}}_{{.LastName}}")
	defer viper.Reset()
	repoName, err = s.RepoName()
	if err != nil {
		t.Fatalf("Failed to get RepoName: %s", err)
	}
	if repoName != "hw_Vinnie_Magro" {
		t.Fatalf("Expected repo name to be hw_Vinnie_Magro, got %s", repoName)
	}
}

func TestRepoNameInvalidTemplate(t *testing.T) {
	// we don't actually need any student data for the broken template error
	s := Student{}
	viper.Set("RepoNameTemplate", "{{.NonExistent}")
	defer viper.Reset()
	_, err := s.RepoName()
	if err == nil {
		t.Fatal("Should have failed with invalid template")
	}
}

func TestRepoUrl(t *testing.T) {
	s := Student{
		UnixName: "smagro",
	}
	viper.Set("RepoNameTemplate", "hw_{{.UnixName}}")
	viper.Set("BotUsername", "bot")
	viper.Set("BotToken", "token")
	viper.Set("GithubOrg", "org")
	defer viper.Reset()
	repoURL, err := s.RepoURL()
	if err != nil {
		t.Fatalf("Failed to get RepoName: %s", err)
	}
	if repoURL.String() != "https://bot:token@github.com/org/hw_smagro.git" {
		t.Fatalf("Got unexpected repo url: %s", repoURL)
	}
}

func TestString(t *testing.T) {
	s := Student{
		UnixName:      "smagro",
		UscID:         "12345",
		PreferredName: "Vinnie",
		Github:        "vmagro",
		FirstName:     "Stephen",
		LastName:      "Magro",
	}
	if s.String() != "Vinnie Magro <smagro>" {
		t.Fatalf("Expected 'Vinnie Magro <smagro>' got '%s'", s.String())
	}
}
