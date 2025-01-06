build-SibylKbLayer:
	# Installing dependencies for ChromaDB 
	mkdir -p "$(ARTIFACTS_DIR)/python"
	python -m pip install -r requirements.txt -t "$(ARTIFACTS_DIR)/python"

	# Sibyl KB Querier class
	mkdir -p "$(ARTIFACTS_DIR)/python/kb"
	cp $(PATH_TO_PROJECT)/kb/__init__.py "$(ARTIFACTS_DIR)/python/kb/"
	cp $(PATH_TO_PROJECT)/kb/kb_topic.py "$(ARTIFACTS_DIR)/python/kb/"
	cp $(PATH_TO_PROJECT)/kb/numi_kb.py "$(ARTIFACTS_DIR)/python/kb/"
	cp $(PATH_TO_PROJECT)/kb/numi_kb_querier.py "$(ARTIFACTS_DIR)/python/kb/"
	
	# Sibyl KB
	mkdir -p "$(ARTIFACTS_DIR)/python/vector_db"
	cp -r $(PATH_TO_PROJECT)/vector_db/* "$(ARTIFACTS_DIR)/python/vector_db/"
	
	# Super aggressive cleanup
	find "$(ARTIFACTS_DIR)/python" -type d -name "__pycache__" -exec rm -rf {} +
	find "$(ARTIFACTS_DIR)/python" -type f -name "*.pyc" -delete
	find "$(ARTIFACTS_DIR)/python" -type f -name "*.pyo" -delete
	find "$(ARTIFACTS_DIR)/python" -type f -name "*.pyd" -delete
	find "$(ARTIFACTS_DIR)/python" -type f -name ".gitignore" -delete
	find "$(ARTIFACTS_DIR)/python" -type d -name "tests" -exec rm -rf {} +
	find "$(ARTIFACTS_DIR)/python" -type d -name "test" -exec rm -rf {} +
	find "$(ARTIFACTS_DIR)/python" -type d -name "examples" -exec rm -rf {} +
	find "$(ARTIFACTS_DIR)/python" -type d -name "docs" -exec rm -rf {} +
	find "$(ARTIFACTS_DIR)/python" -type f -name "*.so" ! -name "_sqlite3.so" -delete
	# Remove development files
	find "$(ARTIFACTS_DIR)/python" -type f -name "*.h" -delete
	find "$(ARTIFACTS_DIR)/python" -type f -name "*.c" -delete
	find "$(ARTIFACTS_DIR)/python" -type f -name "*.cpp" -delete
	# Remove unnecessary package data
	find "$(ARTIFACTS_DIR)/python" -type d -name "*.dist-info" -exec rm -rf {} +
	find "$(ARTIFACTS_DIR)/python" -type d -name "*.egg-info" -exec rm -rf {} +
	

.PHONY: build-SibylKbLayer
