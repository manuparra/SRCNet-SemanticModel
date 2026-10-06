# Vocabulary reference

Proposed namespace: `https://w3id.org/srcnet/services#`.

## Classes

| Term | Meaning |
|---|---|
| `sv:Service` | Stable logical service, reusing the original catalogue identity. |
| `sv:Deployment` | A service deployed in one environment. Separate from a SiteCaps registration. |
| `sv:Site` | Physical or administrative site within a SRC node; explicit SiteCaps site level. |
| `sv:OperationalProfile` | Lifecycle, observed health, monitoring and maintenance information. |
| `sv:FunctionalProfile` | Functions, standards, interfaces and supported data formats. |
| `sv:AdministrationProfile` | Accountable operator, support, escalation, runbooks and change management. |
| `sv:SecurityProfile` | Authentication and authorisation policy references; never credentials. |
| `sv:ResourceAllocation` | Service allocation or request over a shared infrastructure resource. |
| `sv:InfrastructureResource` | Compute, storage or network resource used by a deployment. |
| `sv:SoftwareRelease` | Version of one software component; chart and application are distinct. |
| `sv:Endpoint` | An interface URL with a role, protocol and evidence status. |
| `sv:Dependency` | Directed dependency of a deployment on a logical service. |
| `sv:Measurement` | Timestamped metric with value, unit, method and evidence. |
| `sv:ServiceObjective` | Target with a comparator and evaluation window; not a measurement. |
| `sv:MaintenanceWindow` | Planned or unplanned downtime interval. |
| `sv:Evidence` | Source and date of a report, observation, proposal or synthetic fixture. |
| `sv:SiteCapsRecord` | Version-bound projection of a SiteCaps local/global service object. |
| `sv:RegistrationContext` | Parent node/site/compute identifiers returned by SiteCaps. |

## Properties

| Term | Range | Meaning |
|---|---|---|
| `sv:hasDeployment` | `Deployment` | Links a logical service to a deployment. |
| `sv:realizesService` | `Service` | Logical service implemented by this deployment. |
| `sv:hostedAt` | `Site` | Actual hosting site; global scope does not imply hosting at every consumer. |
| `sv:partOfNode` | `https://w3id.org/srcnet#Node` | Node containing this site. |
| `sv:operational` | `OperationalProfile` | Operational description. |
| `sv:functional` | `FunctionalProfile` | Functional description. |
| `sv:administration` | `AdministrationProfile` | Administration description. |
| `sv:security` | `SecurityProfile` | Security description. |
| `sv:allocation` | `ResourceAllocation` | Allocation, requirement or quota; not whole-site capacity. |
| `sv:resource` | `InfrastructureResource` | Shared resource to which an allocation applies. |
| `sv:software` | `SoftwareRelease` | Component release. |
| `sv:endpoint` | `Endpoint` | Service interface. |
| `sv:dependency` | `Dependency` | Dependency assertion with evidence. |
| `sv:targetService` | `Service` | Logical dependency target. |
| `sv:measurement` | `Measurement` | An observed performance value. |
| `sv:objective` | `ServiceObjective` | A proposed or agreed target. |
| `sv:maintenance` | `MaintenanceWindow` | A maintenance interval. |
| `sv:evidence` | `Evidence` | Evidence supporting this entity description. |
| `sv:registration` | `SiteCapsRecord` | External SiteCaps projection. |
| `sv:registrationContext` | `RegistrationContext` | Discovery parent metadata, not deployment ownership. |
| `sv:operator` | `https://schema.org/Organization` | Accountable operating organisation. |
| `sv:authenticatesWith` | `Service` | Authentication service consumed by this service. |
| `sv:consumesService` | `Service` | Consumption without claiming local hosting. |
| `sv:quantity` | `http://qudt.org/schema/qudt/QuantityValue` | Measured, requested or allocated quantity. |
| `sv:scope` | `string` | local or global logical service scope; independent of physical hosting. |
| `sv:serviceKind` | `string` | Open semantic classification; not the SiteCaps type enumeration. |
| `sv:environment` | `string` | Deployment environment: production, preproduction, test or example. |
| `sv:lifecycle` | `string` | reported-deployed, planned, retired or unknown. |
| `sv:health` | `string` | up, degraded, down or unknown; never inferred from the force-disable flag. |
| `sv:evidenceStatus` | `string` | reported, observed, proposed or synthetic. |
| `sv:sourceDate` | `date` | Date of the source information, not a live availability assertion. |
| `sv:function` | `string` | Function provided, independently of implementation. |
| `sv:format` | `string` | Supported data format or MIME type. |
| `sv:protocol` | `string` | Interface or authentication protocol. |
| `sv:endpointRole` | `string` | Role such as portal, API, capabilities, health or metrics. |
| `sv:namespace` | `string` | Kubernetes namespace. |
| `sv:workloadNamespace` | `string` | Namespace for user workload pods. |
| `sv:orchestrator` | `string` | Deployment orchestration technology. |
| `sv:releaseKind` | `string` | application, helm-chart or container-image. |
| `sv:version` | `string` | Version of the identified component. |
| `sv:releaseName` | `string` | Helm release identifier. |
| `sv:repository` | `anyURI` | Source repository URL. |
| `sv:runbook` | `anyURI` | Operator runbook URL. |
| `sv:supportURL` | `anyURI` | Support entry point. |
| `sv:escalation` | `string` | Escalation route or responsible team. |
| `sv:changeManagement` | `string` | Mechanism for reviewing and applying changes. |
| `sv:backupPolicy` | `string` | Backup policy reference or description. |
| `sv:authorizationPolicy` | `anyURI` | Authorisation policy reference. |
| `sv:tokenAudience` | `string` | Expected token audience; not a token. |
| `sv:tokenScope` | `string` | Expected OAuth scope. |
| `sv:allocationKind` | `string` | request, limit, quota or allocated; do not add shared capacities. |
| `sv:resourceKind` | `string` | compute, storage or network. |
| `sv:storageClass` | `string` | Kubernetes storage class. |
| `sv:claimName` | `string` | PVC claim name; namespace must also be supplied. |
| `sv:metric` | `string` | Metric name, e.g. latency-p95, throughput or cpu-cores. |
| `sv:method` | `string` | Measurement method and aggregation definition. |
| `sv:window` | `duration` | Measurement or objective evaluation window. |
| `sv:comparator` | `string` | Objective comparator: <=, >= or =. |
| `sv:dependencyKind` | `string` | hard or soft dependency. |
| `sv:startsAt` | `dateTime` | UTC or offset-aware interval start. |
| `sv:endsAt` | `dateTime` | UTC or offset-aware interval end. |
| `sv:downtimeKind` | `string` | Planned or Unplanned, matching SiteCaps. |
| `sv:reason` | `string` | Maintenance reason. |
| `sv:siteCapsId` | `string` | SiteCaps service UUID; never fabricated for a real deployment. |
| `sv:siteCapsType` | `string` | Exact SiteCaps type from the pinned scope enumeration. |
| `sv:name` | `string` | Name in the SiteCaps object. |
| `sv:prefix` | `string` | SiteCaps URL scheme without separators. |
| `sv:host` | `string` | SiteCaps host, preserved verbatim. |
| `sv:port` | `integer` | SiteCaps port, preserved verbatim. |
| `sv:path` | `string` | SiteCaps endpoint path, preserved verbatim. |
| `sv:isForceDisabled` | `boolean` | SiteCaps administrative force-disable flag. |
| `sv:isMandatory` | `boolean` | SiteCaps local-service mandatory flag. |
| `sv:associatedComputeId` | `string` | Associated compute UUID, distinct from parent_compute_id. |
| `sv:associatedStorageAreaId` | `string` | Associated storage area UUID. |
| `sv:parentNodeName` | `string` | SiteCaps parent_node_name; do not guess from a display label. |
| `sv:parentSiteName` | `string` | SiteCaps parent_site_name. |
| `sv:parentSiteId` | `string` | SiteCaps parent_site_id UUID. |
| `sv:parentComputeId` | `string` | SiteCaps parent_compute_id UUID. |
| `sv:contractVersion` | `string` | SiteCaps contract version against which the record was checked. |
| `sv:otherAttributes` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON` | Lossless SiteCaps extensibility JSON; semantic detail may be linked here. |
| `sv:downtimeJSON` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON` | Lossless original downtime array, including order and extension fields. |
| `sv:extraFields` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON` | Unrecognised fields retained without inventing semantic meaning. |
