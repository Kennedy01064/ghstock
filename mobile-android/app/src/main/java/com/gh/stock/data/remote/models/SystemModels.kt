package com.gh.stock.data.remote.models

import kotlinx.serialization.Serializable

@Serializable
data class OrderSubmissionDeadlineSettingDto(
    val order_submission_deadline_at: String?,
    val order_submission_deadline_note: String?,
    val last_updated: String
)

@Serializable
data class SystemSettingUpdateDto(
    val order_submission_deadline_at: String? = null,
    val order_submission_deadline_note: String? = null
)

@Serializable
data class PendingTasksStatusDto(
    val building_id: Int,
    val has_pending_orders: Boolean,
    val pending_count: Int
)
