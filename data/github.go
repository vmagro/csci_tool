package data

import (
	"context"
	"time"

	"github.com/golang/glog"
	"github.com/google/go-github/github"
	"github.com/spf13/viper"
	"golang.org/x/oauth2"
)

// we only use some methods that go-github provides so we define them in interfaces for easier testing
type repositories interface {
	ListCommits(ctx context.Context, owner, name string, opt *github.CommitsListOptions) ([]*github.RepositoryCommit, *github.Response, error)
}

// Github is csci_tool's github api wrapper
type Github struct {
	Repositories repositories
}

func GetClient() *github.Client {
	accessToken := viper.GetString("BotToken")
	ctx := context.Background()
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: accessToken},
	)
	tc := oauth2.NewClient(ctx, ts)

	return github.NewClient(tc)
}

// LatestCommitBefore gives the latest commit on the master branch before the specified deadline
func (g *Github) LatestCommitBefore(student *Student, deadline time.Time) (*github.RepositoryCommit, error) {
	glog.Infof("Looking for latest commit from %s before %s", student, deadline)
	repoName, err := student.RepoName()
	if err != nil {
		return nil, err
	}
	commits, _, err := g.Repositories.ListCommits(context.Background(), viper.GetString("GithubOrg"), repoName, &github.CommitsListOptions{
		SHA:   "master",
		Until: deadline,
	})
	if err != nil {
		return nil, err
	}
	// Find the latest commit before the given deadline
	// start with max date as the minimum date possible
	maxDate := time.Date(0, 0, 0, 0, 0, 0, 0, time.UTC)
	var latestCommit *github.RepositoryCommit
	for _, commit := range commits {
		// committer date is the one that's harder to overwrite
		date := commit.Commit.Committer.GetDate()
		if date.After(maxDate) {
			maxDate = date
			latestCommit = commit
		}
	}
	return latestCommit, nil
}
