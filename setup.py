import setuptools

setuptools.setup(
    name='PyViscom',
    version='0.0.1',
    description='Python framework used for exercises of the visual computing group at the Ulm University.',
    url='',
    author='Sebastian Hartwig',
    author_email='sebastian.hartwig@uni-ulm.de',
    maintainer='Sebastian Hartwig',
    maintainer_email='sebastian.hartwig@uni-ulm.de',
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'glfw', 'PyOpenGL', 'glm'],
    include_package_data=True
)
