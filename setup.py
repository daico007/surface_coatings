from setuptools import setup
setup(name="surface_coatings",
      version="0.1.0", 
      descriptions="Generic method to build coated surfaces", 
      author="Co D. Quach", 
      author_email="daico007@gmail.com", 
      license="MIT",
      packages=["surface_coatings"],
      zip_safe=False,
      entry_points={
            "mbuild.plugins": [
                ""
            ]
        }
    )