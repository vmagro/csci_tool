package data

import (
	"context"
	"fmt"
	"testing"
	"time"

	"github.com/google/go-github/github"
	"github.com/spf13/viper"
)

type mockGithubRepositories struct {
}

func (mockGithubRepositories) Get(ctx context.Context, owner, repo string) (*github.Repository, *github.Response, error) {
	if owner == "test-org" && repo == "test-repo" {
		return &github.Repository{
			Owner: &github.User{Login: &owner},
			Name:  &repo,
		}, nil, nil
	}
	return nil, nil, fmt.Errorf("No repo %s/%s", owner, repo)
}

func strPointer(in string) *string {
	return &in
}

func date(month time.Month, day, hour, minute int) *time.Time {
	date := time.Date(2017, month, day, hour, minute, 0, 0, time.UTC)
	return &date
}

func (mockGithubRepositories) ListCommits(ctx context.Context, owner, repo string, opt *github.CommitsListOptions) ([]*github.RepositoryCommit, *github.Response, error) {
	if owner == "test-org" && repo == "hw_smagro" {
		return []*github.RepositoryCommit{
			&github.RepositoryCommit{
				SHA:    strPointer("garbage1"),
				Commit: &github.Commit{Committer: &github.CommitAuthor{Date: date(8, 30, 12, 6)}},
			},
			&github.RepositoryCommit{
				SHA:    strPointer("latest"),
				Commit: &github.Commit{Committer: &github.CommitAuthor{Date: date(10, 30, 12, 6)}},
			},
			&github.RepositoryCommit{
				SHA:    strPointer("garbage2"),
				Commit: &github.Commit{Committer: &github.CommitAuthor{Date: date(10, 30, 12, 5)}},
			},
		}, nil, nil
	}
	return nil, nil, fmt.Errorf("No repo %s/%s", owner, repo)
}

func TestLatestNoSuchRepo(t *testing.T) {
	g := Github{
		mockGithubRepositories{},
	}
	student := Student{
		UnixName: "smagro",
	}
	deadline := time.Now()

	viper.Set("GithubOrg", "test-org")
	viper.Set("RepoNameTemplate", "non-exist")
	defer viper.Reset()
	_, err := g.LatestCommitBefore(&student, deadline)
	if err == nil {
		t.Fatal("Was expecting error for nonexistent repository")
	}
}

func TestLatest(t *testing.T) {
	g := Github{
		mockGithubRepositories{},
	}
	student := Student{
		UnixName: "smagro",
	}
	deadline := time.Now()

	viper.Set("GithubOrg", "test-org")
	viper.Set("RepoNameTemplate", "hw_{{.UnixName}}")
	defer viper.Reset()
	commit, err := g.LatestCommitBefore(&student, deadline)
	if err != nil {
		t.Fatalf("Got unexpected error: %s", err)
	}
	if *commit.SHA != "latest" {
		t.Fatalf("Expected SHA='latest', got '%s'", *commit.SHA)
	}
}
