# Batch vs Streaming

## 1. Nightly Finance Report

Processing: Batch

Reason:
Finance reports process accumulated daily transactions.

Cost of 1-hour staleness:
Reports may be delayed or show incomplete financial results.

## 2. Fraud Detection at Checkout

Processing: Streaming

Reason:
Fraudulent transactions must be detected immediately.

Cost of 1-hour staleness:
Fraudulent payments might be approved, causing financial losses.

## 3. Trending Now Widget

Processing: Streaming / Micro-batch

Reason:
Popularity changes continuously.

Cost of 1-hour staleness:
Users may see outdated trending content.