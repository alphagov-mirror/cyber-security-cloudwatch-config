variable "eu-west-1__sqs__SentMessageSize" {
  description = "List of metrics derived from aws cloudwatch list-metrics"
  type        = list
  default     = []
}

variable "eu-west-2__sqs__SentMessageSize" {
  description = "List of metrics derived from aws cloudwatch list-metrics"
  type        = list
  default     = []
}

resource "aws_cloudwatch_metric_alarm" "euw1_cloudwatch_sqs_sent_message_size" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-1__sqs__SentMessageSize)
  provider            = aws.eu-west-1
  alarm_name          = "${var.eu-west-1__sqs__SentMessageSize[count.index].ResourceName}_SentMessageSize_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  threshold           = var.eu-west-1__sqs__SentMessageSize[count.index].Threshold
  alarm_description   = "Check the maximum size of messages added to the queue."
  metric_name         = "SentMessageSize"
  namespace           = "AWS/SQS"
  period              = 300
  statistic           = "Maximum"
  dimensions = {
    QueueName = var.eu-west-1__sqs__SentMessageSize[count.index].ResourceName
  }
  alarm_actions       = ["${local.euw1_sns_cloudwatch_forwarder_topic}"]
  ok_actions          = ["${local.euw1_sns_cloudwatch_forwarder_topic}"]
  tags                = merge(module.tags.tags, map("Name", "${var.eu-west-1__sqs__SentMessageSize[count.index].ResourceName}_SentMessageSize_alarm_${data.aws_caller_identity.current.account_id}"))
}


resource "aws_cloudwatch_metric_alarm" "euw2_cloudwatch_sqs_sent_message_size" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-2__sqs__SentMessageSize)
  provider            = aws.eu-west-2
  alarm_name          = "${var.eu-west-2__sqs__SentMessageSize[count.index].ResourceName}_SentMessageSize_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  threshold           = var.eu-west-2__sqs__SentMessageSize[count.index].Threshold
  alarm_description   = "Check the maximum size of messages added to the queue."
  metric_name         = "SentMessageSize"
  namespace           = "AWS/SQS"
  period              = 300
  statistic           = "Maximum"
  dimensions = {
    QueueName = var.eu-west-2__sqs__SentMessageSize[count.index].ResourceName
  }
  alarm_actions       = ["${local.euw2_sns_cloudwatch_forwarder_topic}"]
  ok_actions          = ["${local.euw2_sns_cloudwatch_forwarder_topic}"]
  tags                = merge(module.tags.tags, map("Name", "${var.eu-west-2__sqs__SentMessageSize[count.index].ResourceName}_SentMessageSize_alarm_${data.aws_caller_identity.current.account_id}"))
}
