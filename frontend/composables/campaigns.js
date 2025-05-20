import { useApiRequest } from './api';

export const getProjectsDashboard = async () => {
  return await useApiRequest(`/api/projects-dashboard/`);
}

export const getCampaignInfo = async (url_id) => {
  return await useApiRequest(`/api/campaigns/${url_id}/get_campaign_info/`);
};

export const getActivityTimeline = async (url_id) => {
  return await useApiRequest(`/api/campaigns/${url_id}/activity_timeline/`);
}

export const getRecentActivities = async (url_id) => {
  return await useApiRequest(`/api/campaigns/${url_id}/recent_activities/`);
}

export const getCompromiseByCategory = async (url_id) => {
  return await useApiRequest(`/api/campaigns/${url_id}/compromises_by_categories/`);
}
