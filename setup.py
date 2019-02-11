import setuptools

setuptools.setup(
    name='ViscomFramework',
    version='0.0.1',
    description='collection of usefull stuff',
    url='',
    author='Sebastian Hartwig',
    author_email='sebastian.hartwig@uni-ulm.de',
    maintainer='Sebastian Hartwig',
    maintainer_email='sebastian.hartwig@uni-ulm.de',
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'pyrr', 'glfw', 'PyOpenGL'],
    include_package_data=True
)
