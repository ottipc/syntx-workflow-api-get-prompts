# SYNTX Queue CLI Tools

Quick reference for queue management scripts.

## 📊 Status Check
```bash
./scripts/queue_status.sh
```

Shows current queue state across all folders.

## 🧹 Cleanup
```bash
./scripts/queue_cleanup.sh
```

- Recovers stuck jobs from processing/
- Archives old processed jobs (>7 days)

## 🔄 Manual Retry
```bash
# Show usage
./scripts/manual_retry.sh

# Retry all errors
./scripts/manual_retry.sh all

# Retry specific pattern
./scripts/manual_retry.sh fotografie
```

Moves error jobs back to incoming/ for retry.

## 🏭 Force Producer
```bash
./scripts/producer_force.sh
```

Forces producer to generate 20 prompts regardless of queue state.
Use with caution - can cause OVERFLOW if consumer is slow.

---

**Pro Tip:** Run `queue_status.sh` frequently to monitor system health!
