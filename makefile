.PHONY: help

## >>> MAKEFILE <<<
## 
## ---------------------------------------------------------------------
## This file contains commands for setting up the environment as well as
## maintaining it. For more information regarding each command, please
## refer to the README.
## ---------------------------------------------------------------------
## 

help:                    ## Show this help.
	@echo ''
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)
	@echo ''

bash-scripts-executable: ## Make bash files within ./scripts/bash/ executable.
	@find ./scripts/bash/ -type f -iname "*.sh" -exec chmod +x {} \;
	@echo "All bash scripts in ${pwd}/scripts/bash are now executable"

init:                    ## Run all init commands.
	@$(MAKE) bash-scripts-executable
