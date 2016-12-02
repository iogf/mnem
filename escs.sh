# clone mnemosyne.

cd ~/projects/
git clone git@github.com:iogf/mnem.git mnem-code

# push, update, <snippet>
cd ~/projects/mnem-code
git status
git add *
git commit -a
git push
##############################################################################
cd ~/projects/mnem-code
python setup.py sdist register upload
rm -fr dist


