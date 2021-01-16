# COMP0104 - Repated-SStuBs-Analysis

To run the notebook, run `$ jupyter notebook --NotebookApp.iopub_data_rate_limit=1e10` in the command line in the project folder (Jupyter must be installed). A browser tab will open. In that, open `visualization_notebook.py`


See PDF file for report.

## Abstract
This paper presents a comprehensive study of
bug locality within the ManySStuBs4J dataset. By applying
the locality sensitive hashing (LSH) algorithm, we identify repeated SStuBs across the dataset and classify these into clonegroups/buckets. Upon these groups we analyzed the time and
package locality. From our findings we observe that in 63%
of the examined projects, all buckets constrain themselves to
a single package. Furthermore, our findings also conclude that
time locality is important: for 90% of the projects, more than
80% of repeated SStuBs are patched within the same day.
From our results we conclude that package and time-locality
are two important factors in bug detection. Our results can
go towards improving automated program repair tools and
providing developers with the information to prevent these bugs
from occurring.
