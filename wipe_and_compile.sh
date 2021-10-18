pip3 uninstall strato-dyndns -y
rm -rf dist/ build/ *.egg-info
python3 setup.py bdist_wheel
pip3 install dist/*.whl