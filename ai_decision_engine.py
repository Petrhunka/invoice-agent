"""
AI Decision Engine for Invoice Payment Extension Requests
Implements weighted scoring algorithm with risk and confidence calculations
"""

import time
from config import (
    FEATURE_WEIGHTS, CASH_FLOW_RISK, PRIORITY_RISK,
    DECISION_RULES
)


class AIDecisionEngine:
    """AI engine for making payment extension decisions"""
    
    def __init__(self):
        """Initialize the AI decision engine"""
        self.weights = FEATURE_WEIGHTS
        self.rules = DECISION_RULES
    
    def make_decision(self, request_data):
        """
        Make an AI decision for a payment extension request
        
        Args:
            request_data: Dictionary containing request information
        
        Returns:
            Dictionary with decision, confidence, risk, reasoning, and timing
        """
        start_time = time.time()
        
        # Extract features
        amount = float(request_data.get('invoice_amount', 0))
        extension_days = int(request_data.get('requested_extension_days', 0))
        vendor_reliability = float(request_data.get('vendor_reliability_score', 0))
        payment_history = float(request_data.get('payment_history_score', 0))
        cash_flow = request_data.get('cash_flow_impact', 'Medium')
        priority = request_data.get('priority', 'Medium')
        
        # Calculate normalized features
        normalized_features = self._normalize_features(
            amount, extension_days, vendor_reliability, 
            payment_history, cash_flow, priority
        )
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(normalized_features)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            vendor_reliability, payment_history, amount
        )
        
        # Determine decision
        decision = self._determine_decision(
            confidence_score, risk_score, amount
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            decision, confidence_score, risk_score, 
            amount, extension_days, vendor_reliability, payment_history
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare factor details for explanation
        factor_details = self._prepare_factor_details(
            amount, extension_days, vendor_reliability,
            payment_history, cash_flow, priority,
            normalized_features
        )
        
        return {
            'decision': decision,
            'confidence_score': round(confidence_score, 2),
            'risk_score': round(risk_score, 2),
            'reasoning': reasoning,
            'processing_time': round(processing_time, 2),
            'factor_details': factor_details,
            'normalized_features': normalized_features
        }
    
    def _normalize_features(self, amount, extension_days, vendor_reliability,
                           payment_history, cash_flow, priority):
        """Normalize all features to 0-1 scale"""
        
        # Amount risk: normalized by $50,000 threshold
        amount_risk = min(amount / 50000.0, 1.0)
        
        # Extension risk: normalized by 30 days max
        extension_risk = min(extension_days / 30.0, 1.0)
        
        # Vendor risk: inverse of reliability (high reliability = low risk)
        vendor_risk = 1.0 - vendor_reliability
        
        # Payment risk: inverse of payment history
        payment_risk = 1.0 - payment_history
        
        # Cash flow risk: mapped values
        cash_flow_risk = CASH_FLOW_RISK.get(cash_flow, 0.5)
        
        # Priority risk: mapped values
        priority_risk = PRIORITY_RISK.get(priority, 0.5)
        
        return {
            'amount_risk': amount_risk,
            'extension_risk': extension_risk,
            'vendor_risk': vendor_risk,
            'payment_risk': payment_risk,
            'cash_flow_risk': cash_flow_risk,
            'priority_risk': priority_risk
        }
    
    def _calculate_risk_score(self, normalized_features):
        """
        Calculate weighted risk score
        Risk = (Amount × 0.25) + (Extension × 0.20) + (Vendor × 0.20) 
             + (Payment × 0.15) + (CashFlow × 0.15) + (Priority × 0.05)
        """
        risk_score = (
            normalized_features['amount_risk'] * self.weights['amount'] +
            normalized_features['extension_risk'] * self.weights['extension'] +
            normalized_features['vendor_risk'] * self.weights['vendor'] +
            normalized_features['payment_risk'] * self.weights['payment'] +
            normalized_features['cash_flow_risk'] * self.weights['cash_flow'] +
            normalized_features['priority_risk'] * self.weights['priority']
        )
        
        return risk_score
    
    def _calculate_confidence_score(self, vendor_reliability, payment_history, amount):
        """
        Calculate confidence score based on vendor metrics
        Base = (vendor_reliability + payment_history) / 2
        Amount_Factor = 1.0 - min(amount / 100000, 0.3)
        Confidence = Base × Amount_Factor
        """
        base_confidence = (vendor_reliability + payment_history) / 2.0
        amount_factor = 1.0 - min(amount / 100000.0, 0.3)
        confidence = base_confidence * amount_factor
        
        return confidence
    
    def _determine_decision(self, confidence, risk, amount):
        """
        Determine final decision based on confidence and risk scores
        
        Decision Logic:
        - If confidence ≥ 0.80 and risk < 0.4 → Approved
        - If confidence < 0.60 or risk > 0.7 (and amount > 50000) → Escalate
        - If confidence < 0.60 or risk > 0.7 (and amount ≤ 50000) → Rejected
        - If risk < 0.6 and confidence > 0.6 → Approved
        - Else → Escalate
        """
        
        # High confidence and low risk = Auto approve
        if confidence >= self.rules['auto_approve_threshold'] and risk < self.rules['low_risk_threshold']:
            return 'Approved'
        
        # Low confidence or high risk
        if confidence < self.rules['min_confidence_score'] or risk > self.rules['escalate_risk_threshold']:
            if amount > self.rules['high_risk_amount']:
                return 'Escalate'
            else:
                return 'Rejected'
        
        # Moderate confidence and moderate-low risk
        if risk < 0.6 and confidence > self.rules['min_confidence_score']:
            return 'Approved'
        
        # Default to escalation for uncertain cases
        return 'Escalate'
    
    def _generate_reasoning(self, decision, confidence, risk, amount, 
                           extension_days, vendor_reliability, payment_history):
        """Generate human-readable reasoning for the decision"""
        
        reasoning_parts = []
        
        if decision == 'Approved':
            reasoning_parts.append(f"✅ Request APPROVED with {confidence*100:.0f}% confidence.")
            reasoning_parts.append(f"Risk assessment: {risk*100:.0f}% (acceptable level).")
            
            if vendor_reliability > 0.85:
                reasoning_parts.append(f"Vendor has excellent reliability ({vendor_reliability*100:.0f}%).")
            if payment_history > 0.85:
                reasoning_parts.append(f"Strong payment history ({payment_history*100:.0f}%).")
            if amount < 20000:
                reasoning_parts.append(f"Amount ${amount:,.2f} is within low-risk threshold.")
            if extension_days <= 14:
                reasoning_parts.append(f"Short extension period ({extension_days} days) is reasonable.")
                
        elif decision == 'Rejected':
            reasoning_parts.append(f"❌ Request REJECTED due to elevated risk factors.")
            reasoning_parts.append(f"Risk assessment: {risk*100:.0f}% (above acceptable threshold).")
            reasoning_parts.append(f"Confidence level: {confidence*100:.0f}%.")
            
            if vendor_reliability < 0.70:
                reasoning_parts.append(f"⚠️ Vendor reliability concerns ({vendor_reliability*100:.0f}%).")
            if payment_history < 0.70:
                reasoning_parts.append(f"⚠️ Payment history needs improvement ({payment_history*100:.0f}%).")
            if amount > 50000:
                reasoning_parts.append(f"⚠️ High invoice amount: ${amount:,.2f}.")
            if extension_days > 21:
                reasoning_parts.append(f"⚠️ Extended period requested ({extension_days} days).")
                
        else:  # Escalate
            reasoning_parts.append(f"⚡ Request flagged for ESCALATION to human review.")
            reasoning_parts.append(f"Confidence: {confidence*100:.0f}%, Risk: {risk*100:.0f}%.")
            reasoning_parts.append("Factors require management approval due to complexity or amount.")
            
            if amount > 50000:
                reasoning_parts.append(f"💰 High-value transaction: ${amount:,.2f}.")
        
        return " ".join(reasoning_parts)
    
    def _prepare_factor_details(self, amount, extension_days, vendor_reliability,
                                payment_history, cash_flow, priority, normalized):
        """Prepare detailed factor information for explanation views"""
        
        return {
            'amount': {
                'raw_value': amount,
                'normalized': normalized['amount_risk'],
                'weight': self.weights['amount'],
                'contribution': normalized['amount_risk'] * self.weights['amount']
            },
            'extension': {
                'raw_value': extension_days,
                'normalized': normalized['extension_risk'],
                'weight': self.weights['extension'],
                'contribution': normalized['extension_risk'] * self.weights['extension']
            },
            'vendor': {
                'raw_value': vendor_reliability,
                'normalized': normalized['vendor_risk'],
                'weight': self.weights['vendor'],
                'contribution': normalized['vendor_risk'] * self.weights['vendor']
            },
            'payment': {
                'raw_value': payment_history,
                'normalized': normalized['payment_risk'],
                'weight': self.weights['payment'],
                'contribution': normalized['payment_risk'] * self.weights['payment']
            },
            'cash_flow': {
                'raw_value': cash_flow,
                'normalized': normalized['cash_flow_risk'],
                'weight': self.weights['cash_flow'],
                'contribution': normalized['cash_flow_risk'] * self.weights['cash_flow']
            },
            'priority': {
                'raw_value': priority,
                'normalized': normalized['priority_risk'],
                'weight': self.weights['priority'],
                'contribution': normalized['priority_risk'] * self.weights['priority']
            }
        }

