from distutils.core import setup, Extension

def main():
    setup(name="rdrand",
          version="0.1.0",
          description="Python interface for rdrand",
          long_description="https://www.amd.com/system/files/TechDocs/amd-random-number-generator.pdf",
          author="Wojciech Lawren",
          author_email="wojciech[at]lawren.eu",
          license="LGPL v3",
          ext_modules=[Extension("rdrand", ["rdrand.c"])])

if __name__ == "__main__":
    main()
