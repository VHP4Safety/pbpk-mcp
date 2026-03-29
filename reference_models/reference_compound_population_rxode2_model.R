`%||%` <- function(lhs, rhs) {
  if (is.null(lhs)) {
    rhs
  } else {
    lhs
  }
}

.safe_chr <- function(value, default = NULL) {
  if (is.null(value) || length(value) == 0) {
    return(default)
  }
  text <- as.character(value[[1]])
  if (!nzchar(text)) {
    return(default)
  }
  text
}

.safe_num <- function(value, default = 0) {
  number <- suppressWarnings(as.numeric(value[[1]] %||% value))
  if (!is.finite(number)) {
    return(default)
  }
  number
}

.text_values <- function(value) {
  if (is.null(value)) {
    return(character())
  }
  if (is.character(value)) {
    return(Filter(nzchar, value))
  }
  if (is.list(value)) {
    text <- unlist(lapply(value, as.character), use.names = FALSE)
    return(Filter(nzchar, text))
  }
  Filter(nzchar, as.character(value))
}

.default_output_paths <- function() {
  c(
    "Plasma|ReferenceCompound|Concentration",
    "Kidney|Blood|ReferenceCompound|Concentration",
    "Kidney|Tissue|ReferenceCompound|Concentration",
    "Kidney|Filtrate|ReferenceCompound|Concentration",
    "Urine|ReferenceCompound|Amount"
  )
}

.supported_sampling_modes <- function() {
  c("bounded-normal")
}

.validation_parameter_bounds <- function() {
  list(
    "Physiology|BodyWeight" = list(lower = 40, upper = 130, unit = "kg"),
    "Physiology|PlasmaVolumePerKg" = list(lower = 0.02, upper = 0.08, unit = "L/kg"),
    "Physiology|KidneyVolumePerKg" = list(lower = 0.002, upper = 0.02, unit = "L/kg"),
    "Flow|KidneyFlowFraction" = list(lower = 0.05, upper = 0.35, unit = "unitless"),
    "Binding|UnboundFractionPlasma" = list(lower = 0.05, upper = 1, unit = "unitless"),
    "Partition|KidneyToPlasma" = list(lower = 0.5, upper = 8, unit = "unitless"),
    "Kinetics|ClearancePerKg" = list(lower = 0.02, upper = 0.5, unit = "L/h/kg"),
    "Kinetics|KidneyExchangeRate" = list(lower = 0.1, upper = 6, unit = "1/h"),
    "Kinetics|UrineClearanceFraction" = list(lower = 0.05, upper = 0.95, unit = "unitless"),
    "Dose|InfusionAmount" = list(lower = 1, upper = 500, unit = "umol"),
    "Dose|InfusionDuration" = list(lower = 0.05, upper = 24, unit = "h"),
    "Simulation|EndTime" = list(lower = 1, upper = 240, unit = "h"),
    "Simulation|SamplingStep" = list(lower = 0.01, upper = 6, unit = "h")
  )
}

.default_parameters_list <- function() {
  list(
    "Physiology|BodyWeight" = 70,
    "Physiology|PlasmaVolumePerKg" = 0.043,
    "Physiology|KidneyVolumePerKg" = 0.0044,
    "Flow|KidneyFlowFraction" = 0.18,
    "Binding|UnboundFractionPlasma" = 0.75,
    "Partition|KidneyToPlasma" = 2.4,
    "Kinetics|ClearancePerKg" = 0.12,
    "Kinetics|KidneyExchangeRate" = 1.6,
    "Kinetics|UrineClearanceFraction" = 0.35,
    "Dose|InfusionAmount" = 110,
    "Dose|InfusionDuration" = 1,
    "Simulation|EndTime" = 24,
    "Simulation|SamplingStep" = 0.1
  )
}

.parameter_table_defaults <- function() {
  list(
    list(
      path = "Physiology|BodyWeight",
      display_name = "Adult body weight",
      unit = "kg",
      category = "physiology",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Anchors adult human physiology for the bounded rehearsal model.",
      experimentalConditions = c("adult", "human")
    ),
    list(
      path = "Physiology|PlasmaVolumePerKg",
      display_name = "Plasma volume per body weight",
      unit = "L/kg",
      category = "physiology",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Provides a simple adult plasma volume scaling rule for the reference model.",
      experimentalConditions = c("adult", "human")
    ),
    list(
      path = "Physiology|KidneyVolumePerKg",
      display_name = "Kidney volume per body weight",
      unit = "L/kg",
      category = "physiology",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Provides a bounded kidney tissue volume for internal-dose demonstration runs.",
      experimentalConditions = c("adult", "human")
    ),
    list(
      path = "Flow|KidneyFlowFraction",
      display_name = "Kidney flow fraction",
      unit = "unitless",
      category = "physiology",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Represents a bounded share of central distribution routed through the kidney compartment."
    ),
    list(
      path = "Binding|UnboundFractionPlasma",
      display_name = "Plasma unbound fraction",
      unit = "unitless",
      category = "binding",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Used to derive a filtrate-facing concentration signal without claiming a measured binding dataset."
    ),
    list(
      path = "Partition|KidneyToPlasma",
      display_name = "Kidney-to-plasma partition coefficient",
      unit = "unitless",
      category = "partition",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Controls enrichment of the kidney tissue compartment in the synthetic reference workflow."
    ),
    list(
      path = "Kinetics|ClearancePerKg",
      display_name = "Clearance per body weight",
      unit = "L/h/kg",
      category = "kinetics",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Provides a simple body-weight-scaled elimination term for the central compartment."
    ),
    list(
      path = "Kinetics|KidneyExchangeRate",
      display_name = "Kidney exchange rate",
      unit = "1/h",
      category = "kinetics",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Controls reversible exchange between plasma and kidney tissue."
    ),
    list(
      path = "Kinetics|UrineClearanceFraction",
      display_name = "Urinary clearance fraction",
      unit = "unitless",
      category = "kinetics",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Partitions central clearance into urine-facing and non-urine sinks."
    ),
    list(
      path = "Dose|InfusionAmount",
      display_name = "Infusion amount",
      unit = "umol",
      category = "dose",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Defines a bounded demonstration infusion amount for deterministic and population runs.",
      experimentalConditions = c("intravenous infusion")
    ),
    list(
      path = "Dose|InfusionDuration",
      display_name = "Infusion duration",
      unit = "h",
      category = "dose",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Defines the infusion window for the synthetic reference scenario.",
      experimentalConditions = c("intravenous infusion")
    ),
    list(
      path = "Simulation|EndTime",
      display_name = "Simulation end time",
      unit = "h",
      category = "simulation",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Bounds the time horizon for the internal MCP rehearsal run."
    ),
    list(
      path = "Simulation|SamplingStep",
      display_name = "Sampling step",
      unit = "h",
      category = "simulation",
      source = "Synthetic MCP reference defaults",
      sourceType = "demonstration-default",
      evidenceType = "synthetic-reference",
      rationale = "Sets the deterministic integration grid used by the synthetic reference model."
    )
  )
}

.model_assumptions <- function() {
  c(
    "This is a synthetic adult human IV infusion reference model for MCP rehearsal and not a chemical-specific dossier.",
    "The model uses a central and kidney tissue amount balance with urine accumulation and a generic non-urine sink.",
    "Parameter defaults and bounds are demonstration-oriented and must not be interpreted as measured data."
  )
}

.unsupported_uses <- function() {
  c(
    "Direct regulatory dose derivation",
    "Cross-species extrapolation",
    "Pediatric or pregnancy extrapolation",
    "Chemical-specific decision support without a real evidence package"
  )
}

.population_variability_paths <- function() {
  c(
    "Physiology|BodyWeight",
    "Binding|UnboundFractionPlasma",
    "Partition|KidneyToPlasma",
    "Kinetics|ClearancePerKg",
    "Kinetics|KidneyExchangeRate"
  )
}

.missing_qualification_evidence <- function() {
  c(
    "No chemical-specific parameter provenance package is attached.",
    "No observed-versus-predicted or external predictive dataset is bundled.",
    "No external peer review or regulatory-use traceability is declared."
  )
}

.make_validation_issue <- function(code, message, field = NULL, severity = "error") {
  list(
    code = code,
    message = message,
    field = field,
    severity = severity
  )
}

.coerce_parameters <- function(parameters) {
  defaults <- .default_parameters_list()
  resolved <- defaults
  for (path in names(parameters %||% list())) {
    resolved[[path]] <- .safe_num(parameters[[path]], defaults[[path]] %||% 0)
  }
  resolved
}

.parameter_catalog_entry <- function(path, display_name, unit, category) {
  list(
    path = path,
    display_name = display_name,
    unit = unit,
    category = category,
    is_editable = TRUE
  )
}

pbpk_model_metadata <- function() {
  list(
    name = "Reference compound population model",
    modelVersion = "2026-03-30-reference-rxode2",
    createdBy = "PBPK MCP synthetic reference model"
  )
}

pbpk_parameter_catalog <- function() {
  list(
    "Physiology|BodyWeight" = .parameter_catalog_entry("Physiology|BodyWeight", "Adult body weight", "kg", "physiology"),
    "Physiology|PlasmaVolumePerKg" = .parameter_catalog_entry("Physiology|PlasmaVolumePerKg", "Plasma volume per body weight", "L/kg", "physiology"),
    "Physiology|KidneyVolumePerKg" = .parameter_catalog_entry("Physiology|KidneyVolumePerKg", "Kidney volume per body weight", "L/kg", "physiology"),
    "Flow|KidneyFlowFraction" = .parameter_catalog_entry("Flow|KidneyFlowFraction", "Kidney flow fraction", "unitless", "physiology"),
    "Binding|UnboundFractionPlasma" = .parameter_catalog_entry("Binding|UnboundFractionPlasma", "Plasma unbound fraction", "unitless", "binding"),
    "Partition|KidneyToPlasma" = .parameter_catalog_entry("Partition|KidneyToPlasma", "Kidney-to-plasma partition coefficient", "unitless", "partition"),
    "Kinetics|ClearancePerKg" = .parameter_catalog_entry("Kinetics|ClearancePerKg", "Clearance per body weight", "L/h/kg", "kinetics"),
    "Kinetics|KidneyExchangeRate" = .parameter_catalog_entry("Kinetics|KidneyExchangeRate", "Kidney exchange rate", "1/h", "kinetics"),
    "Kinetics|UrineClearanceFraction" = .parameter_catalog_entry("Kinetics|UrineClearanceFraction", "Urinary clearance fraction", "unitless", "kinetics"),
    "Dose|InfusionAmount" = .parameter_catalog_entry("Dose|InfusionAmount", "Infusion amount", "umol", "dose"),
    "Dose|InfusionDuration" = .parameter_catalog_entry("Dose|InfusionDuration", "Infusion duration", "h", "dose"),
    "Simulation|EndTime" = .parameter_catalog_entry("Simulation|EndTime", "Simulation end time", "h", "simulation"),
    "Simulation|SamplingStep" = .parameter_catalog_entry("Simulation|SamplingStep", "Sampling step", "h", "simulation")
  )
}

pbpk_default_parameters <- function() {
  .default_parameters_list()
}

pbpk_parameter_table <- function(parameters = NULL, parameter_catalog = NULL, ...) {
  resolved <- .coerce_parameters(parameters %||% pbpk_default_parameters())
  catalog <- parameter_catalog %||% pbpk_parameter_catalog()
  lapply(.parameter_table_defaults(), function(entry) {
    path <- entry$path
    entry$value <- resolved[[path]]
    entry$display_name <- .safe_chr(entry$display_name, (catalog[[path]] %||% list())$display_name)
    entry$unit <- .safe_chr(entry$unit, (catalog[[path]] %||% list())$unit)
    entry$category <- .safe_chr(entry$category, (catalog[[path]] %||% list())$category)
    entry
  })
}

pbpk_performance_evidence <- function(...) {
  list(
    list(
      id = "runtime-smoke-deterministic-reference",
      kind = "runtime-smoke",
      status = "declared",
      targetOutput = "Plasma|ReferenceCompound|Concentration",
      metric = "Cmax",
      evidenceLevel = "runtime-only",
      evidenceClass = "runtime-smoke",
      qualificationBasis = "internal-workflow-rehearsal-only",
      acceptanceCriterion = "Deterministic run returns finite plasma and kidney outputs on the declared time grid.",
      summary = "Deterministic runtime smoke evidence is bundled for the synthetic reference model.",
      notes = c(
        "This row proves runtime executability only.",
        "It must not be interpreted as predictive validation or external qualification evidence."
      )
    )
  )
}

.trapezoid_auc <- function(times, values) {
  if (length(times) <= 1) {
    return(0)
  }
  total <- 0
  for (index in 2:length(times)) {
    delta <- times[[index]] - times[[index - 1]]
    if (delta < 0) {
      next
    }
    total <- total + (delta * (values[[index]] + values[[index - 1]]) / 2)
  }
  total
}

.safe_sd <- function(values) {
  if (length(values) <= 1) {
    return(0)
  }
  as.numeric(stats::sd(values))
}

.request_section <- function(section, scalar_key = NULL) {
  if (is.null(section)) {
    return(list())
  }
  if (is.list(section)) {
    return(section)
  }
  if (!is.null(scalar_key)) {
    payload <- list()
    payload[[scalar_key]] <- section
    return(payload)
  }
  list(value = section)
}

.normalize_context_use <- function(value) {
  text <- .safe_chr(value)
  if (is.null(text)) {
    return(NULL)
  }
  tolower(text)
}

pbpk_supported_outputs <- function() {
  .default_output_paths()
}

pbpk_model_profile <- function() {
  bounds <- .validation_parameter_bounds()
  bound_entries <- lapply(names(bounds), function(path) {
    c(list(path = path), bounds[[path]])
  })

  list(
    contextOfUse = list(
      scientificPurpose = "Synthetic adult human internal-dose rehearsal model for deterministic and bounded population MCP workflows.",
      decisionContext = "Research, onboarding, and trust-surface testing only.",
      regulatoryUse = "research-only",
      acceptableUncertainty = "No formal regulatory uncertainty target is declared for this synthetic reference package.",
      confidenceLevelRequired = "Runtime and documentation confidence only; not a regulatory qualification target.",
      repurposingAllowed = FALSE,
      supportedQuestions = c(
        "How the MCP surfaces deterministic and bounded population internal-exposure outputs for a public-safe reference model.",
        "How trust, uncertainty, and claim-boundary metadata travel with an executable reference workflow."
      ),
      unsupportedQuestions = .unsupported_uses()
    ),
    applicabilityDomain = list(
      type = "declared-with-runtime-guardrails",
      qualificationLevel = "research-use",
      status = "partially-characterized",
      compounds = c("reference-compound"),
      species = c("human"),
      lifeStage = c("adult"),
      routes = c("iv-infusion"),
      outputs = pbpk_supported_outputs(),
      tissues = c("plasma", "kidney blood", "kidney tissue", "filtrate", "urine"),
      parameterBounds = bound_entries,
      assumptions = .model_assumptions(),
      exclusions = .unsupported_uses(),
      summary = paste(
        "Adult human synthetic reference model for intravenous infusion scenarios,",
        "with MCP-enforced runtime guardrails and research-use qualification only."
      )
    ),
    modelPerformance = list(
      status = "limited-internal-evaluation",
      targetOutputs = pbpk_supported_outputs(),
      goodnessOfFit = list(
        status = "not-bundled",
        summary = "No observed-versus-predicted dataset is bundled because this is a synthetic public-safe reference model."
      ),
      predictiveChecks = list(
        status = "face-validity-and-smoke-tests-only",
        summary = "Current evidence is limited to runtime smoke tests and qualitative plausibility checks within the declared adult IV reference context."
      ),
      evaluationData = list(
        status = "not-bundled",
        summary = "No external predictive dataset is packaged with this synthetic reference model."
      ),
      missingEvidence = c(
        "Observed-versus-predicted comparisons",
        "Formal acceptance criteria tied to external data",
        "External predictive evaluation datasets"
      ),
      summary = paste(
        "The model is executable and bounded for research use,",
        "but it intentionally does not claim chemical-specific predictive performance."
      )
    ),
    parameterProvenance = list(
      status = "partially-declared",
      sourceTable = "pbpk_parameter_catalog / pbpk_parameter_table",
      coverage = "Named runtime parameters exposed through the MCP contract",
      declaredParameterCount = length(pbpk_default_parameters()),
      provenanceMethod = "Synthetic reference annotations with current values, defaults, runtime bounds, and rationale",
      missingEvidence = c(
        "Chemical-specific literature citations",
        "Parameter optimization traceability",
        "Identifiability analysis"
      ),
      summary = paste(
        "The MCP contract exposes a structured parameter table with current values, defaults, runtime bounds,",
        "and rationale fields for the synthetic reference parameters."
      )
    ),
    uncertainty = list(
      status = "partially-characterized",
      variabilityApproach = list(
        supported = TRUE,
        method = "bounded-normal sampling",
        variedParameters = .population_variability_paths(),
        propagationSampleSize = 24L,
        propagationSeed = 20260330L,
        notes = c(
          "Population sampling clips draws into declared runtime bounds.",
          "Sampling bounds are guardrails for a public-safe reference model, not posterior uncertainty distributions."
        )
      ),
      sensitivityAnalysis = list(
        status = "local-screening-attached",
        method = "one-at-a-time bounded perturbation",
        variedParameters = .population_variability_paths(),
        targetOutputs = c(
          "Plasma|ReferenceCompound|Concentration::Cmax",
          "Plasma|ReferenceCompound|Concentration::AUC0-tlast",
          "Kidney|Tissue|ReferenceCompound|Concentration::Cmax"
        ),
        perturbationFraction = 0.1,
        summary = paste(
          "A bounded one-at-a-time local sensitivity screen is bundled for key plasma and kidney outputs",
          "around the default adult IV synthetic reference scenario."
        )
      ),
      residualUncertainty = c(
        "Reference parameters are synthetic and demonstration-oriented.",
        "Guardrail bounds should not be interpreted as a validated extrapolation envelope."
      ),
      summary = paste(
        "Uncertainty evidence currently combines bounded variability propagation with a local perturbation-based sensitivity screen,",
        "but it does not include formal posterior uncertainty propagation."
      ),
      missingEvidence = .missing_qualification_evidence()
    ),
    implementationVerification = list(
      status = "basic-internal-checks",
      codeAvailability = "workspace-source",
      solver = "deterministic explicit time stepping inside the rxode2 worker runtime",
      verifiedChecks = c(
        "Deterministic simulation smoke test",
        "Population simulation smoke test",
        "Runtime guardrail enforcement",
        "Parameter unit consistency check",
        "Systemic flow consistency check",
        "Renal volume consistency check",
        "Executable mass-balance check",
        "Solver stability check"
      ),
      missingChecks = c(
        "Cross-platform numerical regression suite",
        "External solver qualification dossier"
      ),
      notes = c(
        "Implementation verification includes executable structural and numerical checks in addition to smoke tests.",
        "This remains an MCP rehearsal model rather than a regulatory-grade software qualification package."
      )
    ),
    platformQualification = list(
      status = "runtime-platform-documented",
      softwareName = "R synthetic reference module in rxode2 worker",
      softwareVersion = R.version$version.string,
      runtime = "R",
      runtimeVersion = R.version$version.string,
      qualificationBasis = paste(
        "The MCP contract records the R runtime used for execution,",
        "but it does not bundle a formal software-platform qualification package."
      ),
      missingEvidence = c(
        "Formal software-platform qualification dossier",
        "Documented software acceptance criteria and validation record"
      ),
      summary = paste(
        "Execution-platform traceability is declared for the packaged R runtime,",
        "but this remains a research-use runtime record rather than external platform qualification."
      )
    ),
    peerReview = list(
      status = "not-reported",
      priorRegulatoryUse = FALSE,
      revisionStatus = "active-development",
      notes = c(
        "No external peer review or prior regulatory use record is declared for this synthetic reference model."
      )
    ),
    workflowRole = list(
      role = "adult-human-reference-compound-internal-dose-support",
      workflow = "exposure-led-ngra",
      upstreamDependencies = c(
        "Intravenous infusion dose scenario defined outside PBPK MCP.",
        "Synthetic reference parameterization declared in the model profile and parameter table.",
        "Point-of-departure, exposure comparison, and broader NGRA interpretation defined outside PBPK MCP."
      ),
      downstreamOutputs = c(
        "Adult human plasma and kidney internal exposure estimates for the declared synthetic reference outputs.",
        "Bounded adult-like population variability summaries within the declared runtime guardrails.",
        "PBPK qualification, uncertainty, and BER-ready handoff objects when compatible external PoD metadata are attached."
      ),
      nonGoals = c(
        "Standalone exposure assessment ownership.",
        "Chemical-specific regulatory decision support.",
        "Cross-species, pediatric, or pregnancy extrapolation.",
        "Standalone hazard or AOP interpretation."
      )
    ),
    populationSupport = list(
      supportedSpecies = c("human"),
      supportedPhysiologyContexts = c(
        "Adult human physiology under the declared synthetic two-compartment kidney-distribution assumptions."
      ),
      supportedLifeStages = c("adult"),
      supportedGenotypesOrPhenotypes = character(),
      variabilityRepresentation = "declared-or-characterized",
      extrapolationPolicy = "outside-declared-adult-human-reference-context-requires-human-review"
    ),
    evidenceBasis = list(
      basisType = "synthetic-mechanistic-reference-model-with-internal-runtime-evidence",
      inVivoSupportStatus = "not-declared",
      iviveLinkageStatus = "not-declared",
      parameterizationBasis = "synthetic-reference-defaults-and-structured-parameter-table",
      populationVariabilityStatus = "declared-or-characterized"
    ),
    workflowClaimBoundaries = list(
      forwardDosimetry = "supported-within-declared-adult-human-reference-context",
      reverseDosimetry = "not-performed-directly-external-workflow-required",
      exposureLedPrioritization = "supported-only-as-pbpk-substrate-with-external-orchestrator",
      directRegulatoryDoseDerivation = "not-supported"
    ),
    profileSource = list(
      type = "module-self-declared",
      path = "reference_compound_population_rxode2_model.R",
      sourceToolHint = "rxode2",
      summary = "Scientific profile is declared within the MCP-ready synthetic reference model module."
    )
  )
}

pbpk_capabilities <- function() {
  profile <- pbpk_model_profile()
  list(
    backend = "rxode2",
    deterministicSimulation = TRUE,
    populationSimulation = TRUE,
    parameterEditing = TRUE,
    validationHook = TRUE,
    scientificProfile = TRUE,
    supportedOutputs = pbpk_supported_outputs(),
    supportedSampling = .supported_sampling_modes(),
    tags = c("reference-compound", "population", "adult", "synthetic-reference"),
    applicabilityDomain = profile$applicabilityDomain
  )
}

pbpk_validate_request <- function(request = list(), parameters = NULL, stage = NULL, ...) {
  profile <- pbpk_model_profile()
  context_of_use <- profile$contextOfUse %||% list()
  domain_profile <- profile$applicabilityDomain %||% list()
  resolved_parameters <- .coerce_parameters(parameters %||% pbpk_default_parameters())
  bounds <- .validation_parameter_bounds()
  errors <- list()
  warnings <- list()

  add_error <- function(code, message, field = NULL) {
    errors[[length(errors) + 1]] <<- .make_validation_issue(code, message, field, "error")
  }

  add_warning <- function(code, message, field = NULL) {
    warnings[[length(warnings) + 1]] <<- .make_validation_issue(code, message, field, "warning")
  }

  for (path in names(bounds)) {
    value <- as.numeric(resolved_parameters[[path]])
    bound <- bounds[[path]]
    if (!is.finite(value)) {
      add_error("invalid_parameter_value", sprintf("Parameter '%s' must be numeric", path), path)
      next
    }
    if (value < bound$lower || value > bound$upper) {
      add_error(
        "parameter_out_of_bounds",
        sprintf(
          "Value %.4g is outside the supported range %.4g..%.4g %s",
          value,
          bound$lower,
          bound$upper,
          bound$unit
        ),
        path
      )
    }
  }

  if (resolved_parameters[["Simulation|SamplingStep"]] >= resolved_parameters[["Simulation|EndTime"]]) {
    add_error(
      "invalid_sampling_window",
      "Sampling step must be smaller than the simulation end time",
      "Simulation|SamplingStep"
    )
  }

  requested_outputs <- .requested_output_paths(request$outputs %||% list())
  unsupported_outputs <- setdiff(requested_outputs, pbpk_supported_outputs())
  for (path in unsupported_outputs) {
    add_error("unsupported_output", sprintf("Output '%s' is not supported by this model", path), path)
  }

  cohort <- request$cohort %||% list()
  if (!is.null(cohort$size)) {
    size <- suppressWarnings(as.integer(cohort$size))
    if (is.na(size) || size < 1 || size > 200) {
      add_error(
        "cohort_size_out_of_bounds",
        sprintf("Population size must be between 1 and 200; received '%s'", as.character(cohort$size)),
        "cohort.size"
      )
    }
  }

  sampling <- .safe_chr(cohort$sampling)
  if (!is.null(sampling) && !sampling %in% .supported_sampling_modes()) {
    add_error(
      "unsupported_sampling",
      sprintf(
        "Sampling mode '%s' is not supported; expected one of: %s",
        sampling,
        paste(.supported_sampling_modes(), collapse = ", ")
      ),
      "cohort.sampling"
    )
  }

  requested_domain <- .request_section(
    request$applicabilityDomain %||% request$applicability %||% request$domain
  )
  requested_species <- .text_values(requested_domain$species %||% request$species)
  supported_species <- tolower(.text_values(domain_profile$species))
  for (species in requested_species) {
    if (length(supported_species) > 0 && !tolower(species) %in% supported_species) {
      add_error("unsupported_species", sprintf("Species '%s' is outside the declared applicability domain", species), "species")
    }
  }

  requested_life_stage <- .text_values(requested_domain$lifeStage %||% request$lifeStage %||% request$life_stage)
  supported_life_stage <- tolower(.text_values(domain_profile$lifeStage))
  for (life_stage in requested_life_stage) {
    if (length(supported_life_stage) > 0 && !tolower(life_stage) %in% supported_life_stage) {
      add_error("unsupported_life_stage", sprintf("Life stage '%s' is outside the declared applicability domain", life_stage), "lifeStage")
    }
  }

  requested_routes <- .text_values(requested_domain$routes %||% requested_domain$route %||% request$routes %||% request$route)
  supported_routes <- tolower(.text_values(domain_profile$routes))
  for (route in requested_routes) {
    if (length(supported_routes) > 0 && !tolower(route) %in% supported_routes) {
      add_error("unsupported_route", sprintf("Route '%s' is outside the declared applicability domain", route), "route")
    }
  }

  requested_compounds <- .text_values(requested_domain$compounds %||% requested_domain$compound %||% request$compound)
  supported_compounds <- tolower(.text_values(domain_profile$compounds))
  for (compound in requested_compounds) {
    if (length(supported_compounds) > 0 && !tolower(compound) %in% supported_compounds) {
      add_error("unsupported_compound", sprintf("Compound '%s' is outside the declared applicability domain", compound), "compound")
    }
  }

  requested_context <- .request_section(
    request$contextOfUse %||% request$context_of_use,
    scalar_key = "regulatoryUse"
  )
  requested_use <- .normalize_context_use(
    requested_context$regulatoryUse %||% requested_context$intendedUse %||%
      request$regulatoryUse %||% request$intendedUse %||% request$contextOfUse
  )
  declared_use <- .normalize_context_use(context_of_use$regulatoryUse)
  if (!is.null(requested_use) && !is.null(declared_use) && requested_use != declared_use) {
    add_error(
      "context_of_use_mismatch",
      sprintf(
        "Requested context of use '%s' is outside the declared model context '%s'",
        requested_use,
        declared_use
      ),
      "contextOfUse.regulatoryUse"
    )
  }

  if (identical(stage, "load_simulation")) {
    add_warning(
      "runtime_guardrails_only",
      "Applicability checks currently reflect runtime guardrails for this implementation, not external scientific qualification."
    )
    add_warning(
      "research_use_only",
      "Declared context of use is research-only; regulatory or cross-domain use requires additional qualification evidence."
    )
  }

  list(
    ok = length(errors) == 0,
    summary = if (length(errors) == 0) {
      "Request is within the declared runtime guardrails and research-use context"
    } else {
      "Request is outside the declared runtime guardrails or context of use"
    },
    errors = errors,
    warnings = warnings,
    domain = domain_profile,
    assessment = list(
      decision = if (length(errors) == 0) "within-declared-guardrails" else "outside-declared-guardrails",
      guardrailType = domain_profile$type %||% "unspecified",
      qualificationLevel = domain_profile$qualificationLevel %||% "unreported",
      declaredContextOfUse = declared_use %||% "unreported",
      missingEvidence = .missing_qualification_evidence()
    )
  )
}

.requested_output_paths <- function(outputs) {
  candidates <- character()
  if (!is.null(outputs) && length(outputs) > 0) {
    time_series <- outputs$time_series %||% outputs$timeSeries %||% list()
    for (item in time_series) {
      candidates <- c(candidates, as.character(item$path %||% item$parameter %||% item$output %||% NA_character_))
    }
  }
  candidates <- candidates[nzchar(candidates)]
  if (length(candidates) == 0) {
    return(.default_output_paths())
  }
  unique(candidates)
}

.derived_state <- function(parameters) {
  body_weight <- parameters[["Physiology|BodyWeight"]]
  plasma_volume <- body_weight * parameters[["Physiology|PlasmaVolumePerKg"]]
  kidney_volume <- body_weight * parameters[["Physiology|KidneyVolumePerKg"]]
  total_clearance <- body_weight * parameters[["Kinetics|ClearancePerKg"]]
  urine_clearance <- total_clearance * parameters[["Kinetics|UrineClearanceFraction"]]
  other_clearance <- max(total_clearance - urine_clearance, 0)
  kidney_exchange <- parameters[["Kinetics|KidneyExchangeRate"]] * parameters[["Flow|KidneyFlowFraction"]]
  kidney_return <- parameters[["Kinetics|KidneyExchangeRate"]] / max(parameters[["Partition|KidneyToPlasma"]], 1e-6)
  list(
    body_weight = body_weight,
    plasma_volume = plasma_volume,
    kidney_volume = kidney_volume,
    total_clearance = total_clearance,
    urine_clearance = urine_clearance,
    other_clearance = other_clearance,
    kidney_exchange = kidney_exchange,
    kidney_return = kidney_return,
    unbound_fraction = parameters[["Binding|UnboundFractionPlasma"]],
    infusion_amount = parameters[["Dose|InfusionAmount"]],
    infusion_duration = parameters[["Dose|InfusionDuration"]]
  )
}

.time_grid <- function(parameters, step_override = NULL) {
  end_time <- parameters[["Simulation|EndTime"]]
  dt <- step_override %||% parameters[["Simulation|SamplingStep"]]
  seq(0, end_time, by = dt)
}

.run_single <- function(parameters, step_override = NULL) {
  resolved <- .coerce_parameters(parameters)
  state <- .derived_state(resolved)
  times <- .time_grid(resolved, step_override = step_override)
  dt <- times[[2]] - times[[1]]

  central <- numeric(length(times))
  kidney <- numeric(length(times))
  urine <- numeric(length(times))
  other_cleared <- numeric(length(times))
  delivered <- numeric(length(times))

  for (index in 2:length(times)) {
    previous_time <- times[[index - 1]]
    input_rate <- if (previous_time < state$infusion_duration) {
      state$infusion_amount / state$infusion_duration
    } else {
      0
    }
    delivered[[index]] <- delivered[[index - 1]] + (dt * input_rate)

    central_prev <- central[[index - 1]]
    kidney_prev <- kidney[[index - 1]]
    urine_prev <- urine[[index - 1]]
    other_prev <- other_cleared[[index - 1]]

    to_kidney <- state$kidney_exchange * central_prev
    from_kidney <- state$kidney_return * kidney_prev
    urine_loss <- (state$urine_clearance / state$plasma_volume) * central_prev
    other_loss <- (state$other_clearance / state$plasma_volume) * central_prev

    central[[index]] <- max(
      central_prev + dt * (input_rate - to_kidney + from_kidney - urine_loss - other_loss),
      0
    )
    kidney[[index]] <- max(
      kidney_prev + dt * (to_kidney - from_kidney),
      0
    )
    urine[[index]] <- max(urine_prev + dt * urine_loss, 0)
    other_cleared[[index]] <- max(other_prev + dt * other_loss, 0)
  }

  plasma_conc <- central / state$plasma_volume
  kidney_blood_conc <- plasma_conc * state$unbound_fraction
  kidney_tissue_conc <- kidney / state$kidney_volume
  filtrate_conc <- plasma_conc * state$unbound_fraction * 0.85
  mass_balance_error <- max(abs((central + kidney + urine + other_cleared) - delivered), na.rm = TRUE)

  data.frame(
    time = as.numeric(times),
    DoseDelivered = as.numeric(delivered),
    MassBalanceTotal = as.numeric(central + kidney + urine + other_cleared),
    `Plasma|ReferenceCompound|Concentration` = as.numeric(plasma_conc),
    `Kidney|Blood|ReferenceCompound|Concentration` = as.numeric(kidney_blood_conc),
    `Kidney|Tissue|ReferenceCompound|Concentration` = as.numeric(kidney_tissue_conc),
    `Kidney|Filtrate|ReferenceCompound|Concentration` = as.numeric(filtrate_conc),
    `Urine|ReferenceCompound|Amount` = as.numeric(urine),
    stringsAsFactors = FALSE,
    check.names = FALSE
  ) -> result

  attr(result, "mass_balance_error") <- mass_balance_error
  result
}

.series_from_dataframe <- function(df, output_paths) {
  available_units <- list(
    "Plasma|ReferenceCompound|Concentration" = "umol/L",
    "Kidney|Blood|ReferenceCompound|Concentration" = "umol/L",
    "Kidney|Tissue|ReferenceCompound|Concentration" = "umol/L",
    "Kidney|Filtrate|ReferenceCompound|Concentration" = "umol/L",
    "Urine|ReferenceCompound|Amount" = "umol"
  )
  raw_series <- lapply(output_paths, function(path) {
    if (!path %in% names(df)) {
      return(NULL)
    }
    list(
      parameter = path,
      unit = available_units[[path]] %||% "unitless",
      values = lapply(seq_len(nrow(df)), function(index) {
        list(
          time = as.numeric(df$time[[index]]),
          value = as.numeric(df[[path]][[index]])
        )
      })
    )
  })
  Filter(Negate(is.null), raw_series)
}

.deterministic_metric_bundle <- function(parameters, step_override = NULL) {
  solved <- .run_single(parameters, step_override = step_override)
  plasma <- solved[["Plasma|ReferenceCompound|Concentration"]]
  kidney_tissue <- solved[["Kidney|Tissue|ReferenceCompound|Concentration"]]
  times <- solved$time
  stats::setNames(
    list(
      max(plasma, na.rm = TRUE),
      .trapezoid_auc(times, plasma),
      max(kidney_tissue, na.rm = TRUE)
    ),
    c(
      "Plasma|ReferenceCompound|Concentration::Cmax",
      "Plasma|ReferenceCompound|Concentration::AUC0-tlast",
      "Kidney|Tissue|ReferenceCompound|Concentration::Cmax"
    )
  )
}

.perturb_parameter_with_bounds <- function(parameters, path, direction = 1, perturbation_fraction = 0.1) {
  resolved <- .coerce_parameters(parameters)
  current_value <- as.numeric(resolved[[path]])
  bounds <- .validation_parameter_bounds()[[path]] %||% list()
  candidate <- current_value * (1 + (direction * perturbation_fraction))
  if (!is.null(bounds$lower)) {
    candidate <- max(candidate, as.numeric(bounds$lower))
  }
  if (!is.null(bounds$upper)) {
    candidate <- min(candidate, as.numeric(bounds$upper))
  }
  resolved[[path]] <- candidate
  resolved
}

.metric_row_id_fragment <- function(target_output, metric_label) {
  safe_target <- gsub("[^a-z0-9]+", "-", tolower(target_output))
  safe_metric <- gsub("[^a-z0-9]+", "-", tolower(metric_label))
  paste(safe_target, safe_metric, sep = "-")
}

.local_sensitivity_evidence_rows_internal <- function(parameters = NULL) {
  resolved <- .coerce_parameters(parameters %||% pbpk_default_parameters())
  baseline_metrics <- .deterministic_metric_bundle(resolved)
  perturbation_fraction <- 0.1
  parameter_paths <- .population_variability_paths()
  rows <- list()
  detail_records <- list()
  top_driver_notes <- character()

  for (path in parameter_paths) {
    baseline_parameter_value <- as.numeric(resolved[[path]])
    minus_parameters <- .perturb_parameter_with_bounds(resolved, path, direction = -1, perturbation_fraction = perturbation_fraction)
    plus_parameters <- .perturb_parameter_with_bounds(resolved, path, direction = 1, perturbation_fraction = perturbation_fraction)
    minus_parameter_value <- as.numeric(minus_parameters[[path]])
    plus_parameter_value <- as.numeric(plus_parameters[[path]])
    parameter_scale <- max(abs(baseline_parameter_value), 1e-12)
    effective_fraction <- abs(plus_parameter_value - minus_parameter_value) / (2 * parameter_scale)

    minus_metrics <- .deterministic_metric_bundle(minus_parameters)
    plus_metrics <- .deterministic_metric_bundle(plus_parameters)

    for (metric_name in names(baseline_metrics)) {
      metric_tokens <- strsplit(metric_name, "::", fixed = TRUE)[[1]]
      target_output <- metric_tokens[[1]]
      metric_label <- metric_tokens[[2]]
      baseline_value <- as.numeric(baseline_metrics[[metric_name]])
      minus_value <- as.numeric(minus_metrics[[metric_name]])
      plus_value <- as.numeric(plus_metrics[[metric_name]])

      status <- "internal-local-screening"
      sensitivity_value <- NA_real_
      summary <- sprintf(
        "Local sensitivity of %s %s to %s could not be estimated from the bounded perturbation screen.",
        target_output,
        metric_label,
        path
      )

      if (is.finite(baseline_value) && abs(baseline_value) > 1e-12 && is.finite(effective_fraction) && effective_fraction > 0) {
        sensitivity_value <- ((plus_value - minus_value) / baseline_value) / (2 * effective_fraction)
        summary <- sprintf(
          "Local sensitivity of %s %s to %s around the default adult IV reference scenario yielded a normalized coefficient of %.3f.",
          target_output,
          metric_label,
          path,
          sensitivity_value
        )
      } else {
        status <- "warning"
      }

      safe_path <- gsub("[^a-z0-9]+", "-", tolower(path))
      safe_metric <- gsub("[^a-z0-9]+", "-", tolower(metric_label))
      row <- list(
        id = sprintf("local-sensitivity-%s-%s", safe_path, safe_metric),
        kind = "sensitivity-analysis",
        status = status,
        method = "one-at-a-time bounded perturbation",
        targetOutput = target_output,
        metric = metric_label,
        parameterPath = path,
        evidenceLevel = "internal-quantification",
        value = sensitivity_value,
        baselineValue = baseline_value,
        observedValue = minus_value,
        predictedValue = plus_value,
        lowerBound = min(minus_value, plus_value, na.rm = TRUE),
        upperBound = max(minus_value, plus_value, na.rm = TRUE),
        baselineParameterValue = baseline_parameter_value,
        minusParameterValue = minus_parameter_value,
        plusParameterValue = plus_parameter_value,
        perturbationFraction = effective_fraction,
        requestedPerturbationFraction = perturbation_fraction,
        summary = summary,
        notes = c(
          "Positive coefficients indicate that the output increases as the parameter increases around the default scenario.",
          "This is a bounded local screen around the currently declared default parameter set, not a global sensitivity or posterior uncertainty analysis."
        )
      )
      rows[[length(rows) + 1]] <- row
      detail_records[[length(detail_records) + 1]] <- row
    }
  }

  metric_names <- unique(vapply(detail_records, function(entry) {
    paste(entry$targetOutput, entry$metric, sep = "::")
  }, character(1)))

  for (metric_name in metric_names) {
    matching <- Filter(function(entry) {
      identical(paste(entry$targetOutput, entry$metric, sep = "::"), metric_name) &&
        is.finite(as.numeric(entry$value))
    }, detail_records)
    if (length(matching) == 0) {
      next
    }
    best_index <- which.max(vapply(matching, function(entry) abs(as.numeric(entry$value)), numeric(1)))
    best <- matching[[best_index]]
    top_driver_notes <- c(
      top_driver_notes,
      sprintf(
        "Top absolute local driver for %s %s in the default scenario: %s (|NSC|=%.3f).",
        best$targetOutput,
        best$metric,
        best$parameterPath,
        abs(as.numeric(best$value))
      )
    )
  }

  summary_row <- list(
    id = "local-sensitivity-screen-summary",
    kind = "sensitivity-analysis",
    status = "internal-local-screening",
    method = "one-at-a-time bounded perturbation",
    metric = "normalized-sensitivity-coefficient",
    evidenceLevel = "internal-quantification",
    variedParameters = parameter_paths,
    value = if (length(detail_records) > 0) {
      max(vapply(detail_records, function(entry) abs(as.numeric(entry$value)), numeric(1)), na.rm = TRUE)
    } else {
      NA_real_
    },
    summary = sprintf(
      "A bounded one-at-a-time local sensitivity screen was generated for %d parameters across %d deterministic output metrics around the default adult IV reference scenario.",
      length(parameter_paths),
      length(metric_names)
    ),
    notes = c(
      top_driver_notes,
      "Rows in this evidence block report normalized local sensitivity coefficients using guardrail-bounded perturbations around the declared default parameter set.",
      "This improves internal qualification traceability but does not replace global sensitivity analysis, formal uncertainty propagation, or external predictive validation."
    )
  )

  c(list(summary_row), rows)
}

.local_sensitivity_evidence_rows <- function(parameters = NULL) {
  tryCatch(
    .local_sensitivity_evidence_rows_internal(parameters = parameters),
    error = function(exc) {
      list(
        list(
          id = "local-sensitivity-screen-error",
          kind = "sensitivity-analysis",
          status = "failed",
          evidenceLevel = "internal-check",
          summary = sprintf(
            "The bundled local sensitivity screen could not be generated: %s",
            conditionMessage(exc)
          ),
          notes = "OECD report export remains available even if local sensitivity evidence generation fails."
        )
      )
    }
  )
}

.bounded_normal <- function(mean_value, sd_value, lower, upper) {
  value <- stats::rnorm(1, mean = mean_value, sd = sd_value)
  min(max(value, lower), upper)
}

.sample_subject_parameters <- function(parameters, cohort) {
  parameters <- .coerce_parameters(parameters)
  size <- as.integer(cohort$size %||% 1)
  if (size < 1) {
    stop("Population size must be at least 1", call. = FALSE)
  }
  if (size > 200) {
    stop("Population size above 200 is not supported by the rxode2 bridge", call. = FALSE)
  }

  seed <- cohort$seed %||% NULL
  if (!is.null(seed)) {
    set.seed(as.integer(seed))
  }

  subjects <- vector("list", length = size)
  bounds <- .validation_parameter_bounds()
  for (index in seq_len(size)) {
    subject <- parameters
    subject[["Physiology|BodyWeight"]] <- .bounded_normal(
      parameters[["Physiology|BodyWeight"]],
      parameters[["Physiology|BodyWeight"]] * 0.15,
      bounds[["Physiology|BodyWeight"]]$lower,
      bounds[["Physiology|BodyWeight"]]$upper
    )
    subject[["Binding|UnboundFractionPlasma"]] <- .bounded_normal(
      parameters[["Binding|UnboundFractionPlasma"]],
      0.08,
      bounds[["Binding|UnboundFractionPlasma"]]$lower,
      bounds[["Binding|UnboundFractionPlasma"]]$upper
    )
    subject[["Partition|KidneyToPlasma"]] <- .bounded_normal(
      parameters[["Partition|KidneyToPlasma"]],
      0.3,
      bounds[["Partition|KidneyToPlasma"]]$lower,
      bounds[["Partition|KidneyToPlasma"]]$upper
    )
    subject[["Kinetics|ClearancePerKg"]] <- .bounded_normal(
      parameters[["Kinetics|ClearancePerKg"]],
      parameters[["Kinetics|ClearancePerKg"]] * 0.1,
      bounds[["Kinetics|ClearancePerKg"]]$lower,
      bounds[["Kinetics|ClearancePerKg"]]$upper
    )
    subject[["Kinetics|KidneyExchangeRate"]] <- .bounded_normal(
      parameters[["Kinetics|KidneyExchangeRate"]],
      parameters[["Kinetics|KidneyExchangeRate"]] * 0.12,
      bounds[["Kinetics|KidneyExchangeRate"]]$lower,
      bounds[["Kinetics|KidneyExchangeRate"]]$upper
    )
    subjects[[index]] <- subject
  }

  subjects
}

.variability_propagation_evidence_rows_internal <- function(parameters = NULL) {
  resolved <- .coerce_parameters(parameters %||% pbpk_default_parameters())
  sample_size <- 24L
  seed <- 20260330L
  cohort <- list(size = sample_size, seed = seed)
  subjects <- .sample_subject_parameters(resolved, cohort)
  metric_matrix <- lapply(subjects, .deterministic_metric_bundle)
  metric_names <- names(metric_matrix[[1]] %||% list())
  if (length(metric_names) == 0) {
    stop("No deterministic metrics were available for variability propagation evidence", call. = FALSE)
  }

  rows <- list()
  top_uncertainty_notes <- character()
  for (metric_name in metric_names) {
    metric_tokens <- strsplit(metric_name, "::", fixed = TRUE)[[1]]
    target_output <- metric_tokens[[1]]
    metric_label <- metric_tokens[[2]]
    values <- vapply(metric_matrix, function(entry) as.numeric(entry[[metric_name]]), numeric(1))
    q <- stats::quantile(values, probs = c(0.05, 0.5, 0.95), names = FALSE, type = 7, na.rm = TRUE)
    mean_value <- mean(values, na.rm = TRUE)
    sd_value <- .safe_sd(values)
    cv_value <- if (abs(mean_value) > 1e-12) sd_value / abs(mean_value) else 0

    rows[[length(rows) + 1]] <- list(
      id = sprintf("bounded-variability-propagation-%s", .metric_row_id_fragment(target_output, metric_label)),
      kind = "variability-propagation",
      status = "internal-quantification",
      method = "bounded-normal Monte Carlo propagation",
      targetOutput = target_output,
      metric = metric_label,
      evidenceLevel = "internal-quantification",
      sampleSize = sample_size,
      seed = seed,
      variedParameters = .population_variability_paths(),
      value = q[[2]],
      meanValue = mean_value,
      sdValue = sd_value,
      coefficientOfVariation = cv_value,
      p05 = q[[1]],
      p50 = q[[2]],
      p95 = q[[3]],
      lowerBound = q[[1]],
      upperBound = q[[3]],
      summary = sprintf(
        "Bounded variability propagation for %s %s across %d sampled adult scenarios yielded median %.3f with p05-p95 %.3f-%.3f.",
        target_output,
        metric_label,
        sample_size,
        q[[2]],
        q[[1]],
        q[[3]]
      ),
      notes = c(
        "This propagates bounded population variability through the default adult IV synthetic reference scenario using the model's current MCP parameter state.",
        "These rows summarize variability propagation, not posterior uncertainty inference or an externally qualified exposure distribution."
      )
    )

    top_uncertainty_notes <- c(
      top_uncertainty_notes,
      sprintf(
        "%s %s: median %.3f, p05 %.3f, p95 %.3f, CV %.3f.",
        target_output,
        metric_label,
        q[[2]],
        q[[1]],
        q[[3]],
        cv_value
      )
    )
  }

  summary_row <- list(
    id = "bounded-variability-propagation-summary",
    kind = "variability-propagation",
    status = "internal-quantification",
    method = "bounded-normal Monte Carlo propagation",
    metric = "internal-exposure-distribution-summary",
    evidenceLevel = "internal-quantification",
    sampleSize = sample_size,
    seed = seed,
    variedParameters = .population_variability_paths(),
    summary = sprintf(
      "A bounded variability-propagation screen was generated for %d subjects across %d deterministic output metrics using the current loaded reference-model parameter state.",
      sample_size,
      length(metric_names)
    ),
    notes = c(
      top_uncertainty_notes,
      "This provides a compact internal-exposure distribution summary for MCP sessions, but it does not replace formal uncertainty propagation or external qualification studies."
    )
  )

  c(list(summary_row), rows)
}

.variability_propagation_evidence_rows <- function(parameters = NULL) {
  tryCatch(
    .variability_propagation_evidence_rows_internal(parameters = parameters),
    error = function(exc) {
      list(
        list(
          id = "bounded-variability-propagation-error",
          kind = "variability-propagation",
          status = "failed",
          evidenceLevel = "internal-check",
          summary = sprintf(
            "The bounded variability-propagation screen could not be generated: %s",
            conditionMessage(exc)
          ),
          notes = "Uncertainty evidence export remains available even if the variability-propagation bundle fails."
        )
      )
    }
  )
}

pbpk_uncertainty_evidence <- function(parameters = NULL, ...) {
  c(
    .local_sensitivity_evidence_rows(parameters = parameters),
    .variability_propagation_evidence_rows(parameters = parameters)
  )
}

pbpk_verification_evidence <- function(...) {
  list(
    list(
      id = "reference-model-verification-evidence",
      kind = "implementation-verification",
      status = "declared",
      evidenceLevel = "internal-reference",
      summary = "Executable verification rows are bundled for unit consistency, structural checks, mass balance, and solver stability.",
      notes = c(
        "These rows support runtime integrity and trust-surface rehearsal.",
        "They do not imply external predictive validation."
      )
    )
  )
}

pbpk_platform_qualification_evidence <- function(...) {
  list(
    list(
      id = "reference-model-platform-traceability",
      kind = "software-platform",
      status = "declared",
      evidenceLevel = "internal-reference",
      summary = sprintf(
        "The packaged R runtime was recorded as %s for this synthetic reference model.",
        R.version$version.string
      ),
      notes = c(
        "The runtime identity is traceable for MCP release and audit purposes.",
        "No formal external platform qualification package is attached."
      )
    )
  )
}

pbpk_run_verification_checks <- function(parameters = NULL, request = list(), parameter_catalog = NULL, parameter_table = NULL, ...) {
  resolved <- .coerce_parameters(parameters %||% pbpk_default_parameters())
  derived <- .derived_state(resolved)
  deterministic <- .run_single(resolved)
  deterministic_metrics <- .deterministic_metric_bundle(resolved)
  refined_metrics <- .deterministic_metric_bundle(resolved, step_override = max(resolved[["Simulation|SamplingStep"]] / 2, 0.01))
  max_abs_diff <- max(abs(unlist(deterministic_metrics) - unlist(refined_metrics)))
  parameter_rows <- parameter_table$rows %||% parameter_table %||% list()
  non_empty_units <- length(parameter_rows) > 0 && all(vapply(parameter_rows, function(entry) nzchar(.safe_chr(entry$unit, "")), logical(1)))
  mass_balance_error <- attr(deterministic, "mass_balance_error") %||% Inf
  total_flow_fraction <- resolved[["Flow|KidneyFlowFraction"]]
  volume_ratio <- derived$kidney_volume / derived$plasma_volume

  list(
    list(
      id = "parameter-unit-consistency",
      kind = "unit-consistency",
      status = if (non_empty_units) "passed" else "failed",
      summary = if (non_empty_units) {
        "Parameter table rows expose units for the current synthetic reference runtime parameters."
      } else {
        "Parameter table rows were missing one or more unit declarations."
      }
    ),
    list(
      id = "systemic-flow-consistency",
      kind = "structural-consistency",
      status = if (total_flow_fraction > 0 && total_flow_fraction < 1) "passed" else "failed",
      summary = sprintf(
        "Kidney flow fraction remained bounded at %.3f of central distribution.",
        total_flow_fraction
      ),
      value = total_flow_fraction
    ),
    list(
      id = "renal-volume-consistency",
      kind = "structural-consistency",
      status = if (volume_ratio > 0 && volume_ratio < 1) "passed" else "failed",
      summary = sprintf(
        "Kidney volume stayed bounded relative to plasma volume (ratio %.3f).",
        volume_ratio
      ),
      value = volume_ratio
    ),
    list(
      id = "mass-balance",
      kind = "mass-balance",
      status = if (mass_balance_error <= 1e-6) "passed" else "failed",
      summary = sprintf(
        "Mass-balance deviation across the deterministic run remained %.3e umol.",
        mass_balance_error
      ),
      value = mass_balance_error
    ),
    list(
      id = "solver-stability",
      kind = "solver-stability",
      status = if (max_abs_diff <= 1.0) "passed" else "warning",
      summary = sprintf(
        "Refined sampling grid changed the deterministic metric bundle by at most %.3f.",
        max_abs_diff
      ),
      value = max_abs_diff
    )
  )
}

pbpk_run_simulation <- function(parameters, simulation_id = NULL, run_id = NULL, request = list()) {
  output_paths <- .requested_output_paths(request$outputs %||% list())
  resolved_parameters <- .coerce_parameters(parameters)
  solved <- .run_single(resolved_parameters)

  list(
    metadata = list(
      engine = "rxode2",
      sourceModel = "reference_compound_population_rxode2_model.R",
      requestedOutputs = output_paths
    ),
    series = .series_from_dataframe(solved, output_paths)
  )
}

pbpk_run_population <- function(parameters, cohort = list(), outputs = list(), simulation_id = NULL, request = list()) {
  output_paths <- .requested_output_paths(outputs)
  subjects <- .sample_subject_parameters(parameters, cohort)
  metrics <- vector("list", length(subjects))
  subject_series <- vector("list", length(subjects))

  for (index in seq_along(subjects)) {
    solved <- .run_single(subjects[[index]])
    plasma <- solved[["Plasma|ReferenceCompound|Concentration"]]
    times <- solved$time
    cmax <- max(plasma)
    tmax <- times[[which.max(plasma)]]
    auc <- .trapezoid_auc(times, plasma)
    metrics[[index]] <- list(cmax = cmax, tmax = tmax, auc = auc)

    outputs_payload <- lapply(output_paths, function(path) solved[[path]])
    names(outputs_payload) <- output_paths

    subject_series[[index]] <- list(
      subjectId = index,
      time = as.numeric(times),
      outputs = outputs_payload
    )
  }

  cmax_values <- vapply(metrics, function(item) item$cmax, numeric(1))
  tmax_values <- vapply(metrics, function(item) item$tmax, numeric(1))
  auc_values <- vapply(metrics, function(item) item$auc, numeric(1))

  chunk_size <- 25L
  chunk_count <- ceiling(length(subject_series) / chunk_size)
  chunks <- vector("list", chunk_count)
  for (chunk_index in seq_len(chunk_count)) {
    start_index <- ((chunk_index - 1L) * chunk_size) + 1L
    end_index <- min(length(subject_series), chunk_index * chunk_size)
    chunk_subjects <- subject_series[start_index:end_index]
    first_subject <- chunk_subjects[[1]]
    preview_path <- output_paths[[1]]
    chunks[[chunk_index]] <- list(
      chunkId = sprintf("subjects-%03d-%03d", start_index, end_index),
      subjectRange = c(start_index, end_index),
      timeRange = c(0, max(first_subject$time)),
      preview = list(
        output = preview_path,
        subjectId = first_subject$subjectId,
        time = first_subject$time[1:min(5, length(first_subject$time))],
        value = first_subject$outputs[[preview_path]][1:min(5, length(first_subject$outputs[[preview_path]]))]
      ),
      payload = list(
        outputs = output_paths,
        subjects = chunk_subjects
      )
    )
  }

  list(
    aggregates = list(
      meanCmax = mean(cmax_values),
      sdCmax = .safe_sd(cmax_values),
      meanTmax = mean(tmax_values),
      meanAUC = mean(auc_values),
      sdAUC = .safe_sd(auc_values)
    ),
    metadata = list(
      engine = "rxode2",
      sourceModel = "reference_compound_population_rxode2_model.R",
      cohortSize = length(subject_series),
      storedOutputs = output_paths
    ),
    chunks = chunks
  )
}
