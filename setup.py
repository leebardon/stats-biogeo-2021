from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):

    def run(self):
        import shutil, glob
        shutil.rmtree('dist')
        shutil.rmtree(glob.glob('*.egg-info')[0])
        shutil.rmtree(glob.glob('build/bdist.*')[0])
        install.run(self)

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Using Darwin Model output as a testbed to assess the predictive capabilites of statistical learning models. ',
    author='Lee Bardon',
    license='MIT',
    cmdclass = {'install':PostInstallCommand},
)
