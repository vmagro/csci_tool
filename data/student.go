package data

import (
	"bytes"
	"fmt"
	"html/template"
	"net/url"

	"github.com/spf13/viper"
)

// Student represents a single student enrolled in the class
type Student struct {
	UnixName      string
	UscID         string
	PreferredName string
	Github        string
	FirstName     string
	LastName      string
}

// RepoName gets the name of the Student's GitHub repo using a template string.
func (s *Student) RepoName() (string, error) {
	viper.SetDefault("RepoNameTemplate", "hw_{{.UnixName}}")
	repoTemplate, err := template.New("repo").Parse(viper.GetString("RepoNameTemplate"))
	if err != nil {
		return "(null)", err
	}
	var buf bytes.Buffer
	repoTemplate.Execute(&buf, s)
	return buf.String(), nil
}

// RepoURL returns a pre-authenticated cloneable git url to the the Student's repo.
func (s *Student) RepoURL() (*url.URL, error) {
	username := viper.Get("BotUsername")
	token := viper.Get("BotToken")
	githubOrg := viper.Get("GithubOrg")
	repoName, err := s.RepoName()
	if err != nil {
		return nil, err
	}
	urlStr := fmt.Sprintf("http://%s:%s@github.com/%s/%s.git", username, token, githubOrg, repoName)
	url, err := url.Parse(urlStr)
	if err != nil {
		return nil, err
	}
	return url, nil
}

// LoadStudents loads a slice containing a struct for every Student
func LoadStudents() ([]Student, error) {
	return nil, nil
}
