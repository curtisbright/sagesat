
Embedding of the SAGE CAS within a SAT solver.

* Dependencies
    * Glucose SAT solver
    * SAGE (version 6.3)
		* The Ply package for lexing and parsing must be installed on top of SAGE's built-in version of python.
	* sharpSAT (only for matching counts in Table 1)
	* Z3 (purely for Tseitin-encoding, will eventually be removed)
	* Glucose-SAGE extension (https://bitbucket.org/ezulkosk/glucose-sage)
	  	* Copy the glucose executable in core to sagesat/bin

* Locations for Glucose and sharpSAT must be set in src/common/common.py.

* The resolution proof certificate for the matchings case study is too large to upload, and can be distributed as needed. Checks were performed using drup-trim.

* The generated cycles and matchings for Q_5 are located in results/matchings/cycle_data_in. Each pair of consecutive lines correspond to a cycle and the matching it extends.

* Example Runs
	Must be run within the SAGE environment, from the src directory.

	* To run either case study:
		* python main.py ../test/hamilton
		* python main.py ../test/antipodal

	* To obtain matching counts for Table 1:
		* python matching_counts.py