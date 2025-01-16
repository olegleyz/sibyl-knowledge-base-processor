build-SibylInterpLayer:
	# Create fresh directory
	rm -rf "$(ARTIFACTS_DIR)/python" || true
	mkdir -p "$(ARTIFACTS_DIR)/python"

	# Copy KB files
	mkdir -p "$(ARTIFACTS_DIR)/python/interpretations"
	cp $(PATH_TO_PROJECT)/data/output/base_energy_month_kb.json "$(ARTIFACTS_DIR)/python/interpretations/"
	cp $(PATH_TO_PROJECT)/data/output/base_energy_day_kb_single_en.json "$(ARTIFACTS_DIR)/python/interpretations/"

.PHONY: build-SibylKbLayer