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
	repoName, err := s.RepoName()
	if err != nil {
		t.Fatalf("Failed to get RepoName: %s", err)
	}
	if repoName != "hw_smagro" {
		t.Fatalf("Expected repo name to be hw_smagro, got %s", repoName)
	}

	// make sure it also works with a custom template
	viper.Set("RepoNameTemplate", "hw_{{.PreferredName}}_{{.LastName}}")
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
	_, err := s.RepoName()
	if err == nil {
		t.Fatal("Should have failed with invalid template")
	}
}

func TestRepoUrl(t *testing.T) {
	s := Student{
		UnixName:      "smagro",
		UscID:         "12345",
		PreferredName: "Vinnie",
		Github:        "vmagro",
		FirstName:     "Stephen",
		LastName:      "Magro",
	}
	repoName, err := s.RepoName()
	if err != nil {
		t.Fatalf("Failed to get RepoName: %s", err)
	}
	if repoName != "hw_smagro" {
		t.Fatalf("Expected repo name to be hw_smagro, got %s", repoName)
	}
}
