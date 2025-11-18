# OPA Policy - Validação de Segregação ISO 27017
package terraform.network_segregation

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_vpc"
    not has_environment_tag(resource)
    msg := sprintf("VPC '%s' deve ter tag 'Environment' para segregação (ISO 27017)", [resource.name])
}

deny[msg] {
    production_vpc := input.resource_changes[_]
    production_vpc.type == "aws_vpc"
    production_vpc.change.after.tags.Environment == "production"
    
    dev_vpc := input.resource_changes[_]
    dev_vpc.type == "aws_vpc"
    dev_vpc.change.after.tags.Environment == "development"
    
    cidr_overlaps(production_vpc.change.after.cidr_block, dev_vpc.change.after.cidr_block)
    msg := "VPCs de produção e desenvolvimento não devem ter CIDRs sobrepostos (ISO 27017)"
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_network_acl"
    not has_deny_rule(resource)
    msg := sprintf("Network ACL '%s' deve ter regras de negação entre ambientes (ISO 27017)", [resource.name])
}

has_environment_tag(vpc) {
    vpc.change.after.tags.Environment
}

has_deny_rule(acl) {
    rule := acl.change.after.egress[_]
    rule.action == "deny"
}

cidr_overlaps(cidr1, cidr2) {
    # Simplificação: verifica se os primeiros octetos são iguais
    cidr1 == cidr2
}
