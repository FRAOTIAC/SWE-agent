sweagent run-batch \
    --config .config/coding_challenge.yaml \
    --agent.model.per_instance_cost_limit 2.00 \
    --instances.type swe_bench \
    --instances.subset lite \
    --instances.split dev  \
    --instances.shuffle=True \
    --num_workers 3 \
    --instances.evaluate=True
    # --instances.slice :3 \
