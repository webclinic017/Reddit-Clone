output "alb_dns_name" {
  description = "The Application Load Balancer DNS name"
  value       = aws_lb.load_balancer.dns_name
}