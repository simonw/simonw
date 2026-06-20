# php-1.99s

An archived copy of PHP 1.99s - originally released 31st May 1997

Visit [php-1.99s/README](https://github.com/simonw/php-1.99s/blob/main/php-1.99s/README) for the original README.

Here's how I created this copy, using code downloaded from https://museum.php.net/

    mkdir php-1.99s
    cd php-1.99s
    wget https://museum.php.net/php2/php-1.99s.tar.gz
    tar -xzvf php-1.99s.tar.gz
    # Commit code with date of 31st May 1997
    git init
    git add php-1.99s
    git commit \
      --author="PHP History <actions@users.noreply.github.com>" \
      --date="1997-05-31" \
      -m "PHP 1.99s"
    # That set author date but not commit date - this updates that:
    git filter-branch --env-filter 'export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE"'

Then I added a tag to the commit I had just created using:

    git tag -a v1.99s -m "PHP 1.99s"
