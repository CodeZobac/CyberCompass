'use client';

import { useState, useEffect } from 'react';
import { useTranslations } from 'next-intl';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Input } from '../../../components/ui/input';

import Header from '../../../components/Header';

interface Admin {
  id: string;
  user_id: string;
  email: string;
  is_root_admin: boolean;
  can_manage_admins: boolean;
  created_at: string;
  users?: {
    name: string;
    email: string;
  };
  added_by?: {
    users: {
      name: string;
      email: string;
    };
  };
}

interface AdminPermissions {
  isAdmin: boolean;
  isRootAdmin: boolean;
  canManageAdmins: boolean;
}

export default function ManageAdminsPage() {
  const t = useTranslations('admin.users');
  const [admins, setAdmins] = useState<Admin[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [permissions, setPermissions] = useState<AdminPermissions>({
    isAdmin: false,
    isRootAdmin: false,
    canManageAdmins: false
  });

  // Add admin form state
  const [email, setEmail] = useState('');
  const [isRootAdmin, setIsRootAdmin] = useState(false);
  const [canManageAdmins, setCanManageAdmins] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // Check admin permissions
  useEffect(() => {
    const checkPermissions = async () => {
      try {
        const response = await fetch('/api/admin/check');
        const data = await response.json();
        
        if (!data.isAdmin || (!data.isRootAdmin && !data.canManageAdmins)) {
          setError(t('errors.noPermission'));
          setLoading(false);
          return;
        }
        
        setPermissions({
          isAdmin: data.isAdmin,
          isRootAdmin: data.isRootAdmin,
          canManageAdmins: data.canManageAdmins
        });
        
        // Load admins if user has permission
        await loadAdmins();
      } catch (err) {
        console.error('Error checking permissions:', err);
        setError(t('errors.noPermission'));
        setLoading(false);
      }
    };

    checkPermissions();
  }, [t]);

  const loadAdmins = async () => {
    try {
      const response = await fetch('/api/admin/users');
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to load admins');
      }

      setAdmins(data.admins);
      setLoading(false);
    } catch (err) {
      console.error('Error loading admins:', err);
      setError(err instanceof Error ? err.message : 'Failed to load admins');
      setLoading(false);
    }
  };

  const handleAddAdmin = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccess(null);

    if (!email) {
      setError(t('errors.emailRequired'));
      setSubmitting(false);
      return;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError(t('errors.invalidEmail'));
      setSubmitting(false);
      return;
    }

    try {
      const response = await fetch('/api/admin/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          isRootAdmin,
          canManageAdmins,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to add admin');
      }

      setSuccess(t('success.adminAdded'));
      setEmail('');
      setIsRootAdmin(false);
      setCanManageAdmins(false);
      
      // Reload admins list
      await loadAdmins();
    } catch (err) {
      console.error('Error adding admin:', err);
      setError(err instanceof Error ? err.message : t('errors.addFailed'));
    } finally {
      setSubmitting(false);
    }
  };

  const handleRemoveAdmin = async (adminId: string) => {
    if (!confirm(t('confirmRemove'))) {
      return;
    }

    try {
      const response = await fetch(`/api/admin/users/${adminId}`, {
        method: 'DELETE',
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to remove admin');
      }

      setSuccess(t('success.adminRemoved'));
      
      // Reload admins list
      await loadAdmins();
    } catch (err) {
      console.error('Error removing admin:', err);
      setError(err instanceof Error ? err.message : t('errors.removeFailed'));
    }
  };

  const handleTogglePermissions = async (adminId: string, field: 'is_root_admin' | 'can_manage_admins', currentValue: boolean) => {
    try {
      const updateData = {
        [field === 'is_root_admin' ? 'isRootAdmin' : 'canManageAdmins']: !currentValue
      };

      const response = await fetch(`/api/admin/users/${adminId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to update permissions');
      }

      setSuccess(t('success.permissionsUpdated'));
      
      // Reload admins list
      await loadAdmins();
    } catch (err) {
      console.error('Error updating permissions:', err);
      setError(err instanceof Error ? err.message : t('errors.updateFailed'));
    }
  };

  if (loading) {
    return (
      <>
        <Header />
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
          <div className="container mx-auto px-6 py-12">
            <div className="text-center">
              <p className="text-lg text-gray-600">{t('loading')}</p>
            </div>
          </div>
        </div>
      </>
    );
  }

  if (error && !permissions.isAdmin) {
    return (
      <>
        <Header />
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
          <div className="container mx-auto px-6 py-12">
            <Card className="p-8 bg-red-50 border-4 border-red-400">
              <h2 className="text-2xl font-bold text-red-800 mb-4">Access Denied</h2>
              <p className="text-red-700">{error}</p>
            </Card>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
        {/* Header Section */}
        <div className="bg-white border-b-4 border-black shadow-[0_4px_0_0_#000]">
          <div className="container mx-auto px-6 py-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-black text-gray-900 mb-2 tracking-tight">
                  {t('title')}
                </h1>
                <p className="text-lg text-gray-600 max-w-2xl">
                  {t('manageAdminsDesc')}
                </p>
              </div>
              <div className="hidden md:flex items-center space-x-4">
                <div className="bg-purple-100 border-2 border-purple-600 rounded-lg px-4 py-2">
                  <span className="text-purple-800 font-semibold text-sm uppercase tracking-wider">
                    👥 Admin Management
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-6 py-12">
          {/* Error/Success Messages */}
          {error && (
            <div className="mb-6">
              <Card className="p-4 bg-red-50 border-4 border-red-400">
                <p className="text-red-800 font-semibold">{error}</p>
              </Card>
            </div>
          )}

          {success && (
            <div className="mb-6">
              <Card className="p-4 bg-green-50 border-4 border-green-400">
                <p className="text-green-800 font-semibold">{success}</p>
              </Card>
            </div>
          )}

          {/* Add Admin Form */}
          <div className="mb-12">
            <Card className="p-8 bg-gradient-to-br from-purple-50 to-pink-50 border-4 border-purple-400 shadow-[8px_8px_0_0_#8b5cf6]">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                ➕ {t('addAdmin')}
              </h2>
              
              <form onSubmit={handleAddAdmin} className="space-y-6">
                <div>
                  <label htmlFor="email" className="text-lg font-semibold text-gray-900">
                    {t('email')}
                  </label>
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="admin@example.com"
                    className="mt-2 text-lg border-4 border-gray-300 rounded-lg"
                    required
                  />
                </div>

                {permissions.isRootAdmin && (
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <input
                        id="rootAdmin"
                        type="checkbox"
                        checked={isRootAdmin}
                        onChange={(e) => setIsRootAdmin(e.target.checked)}
                        className="w-5 h-5 border-2 border-gray-400 rounded"
                      />
                      <label htmlFor="rootAdmin" className="text-lg font-semibold text-gray-900">
                        {t('makeRoot')}
                      </label>
                    </div>

                    <div className="flex items-center space-x-3">
                      <input
                        id="manageAdmins"
                        type="checkbox"
                        checked={canManageAdmins}
                        onChange={(e) => setCanManageAdmins(e.target.checked)}
                        className="w-5 h-5 border-2 border-gray-400 rounded"
                      />
                      <label htmlFor="manageAdmins" className="text-lg font-semibold text-gray-900">
                        {t('toggleManageAdmins')}
                      </label>
                    </div>
                  </div>
                )}

                <Button
                  type="submit"
                  disabled={submitting}
                  variant="brutal"
                  className="text-lg font-bold tracking-wide uppercase bg-purple-500 hover:bg-purple-600"
                >
                  {submitting ? 'Adding...' : `➕ ${t('add')}`}
                </Button>
              </form>
            </Card>
          </div>

          {/* Current Admins List */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              👥 {t('currentAdmins')}
            </h2>
            
            {admins.length === 0 ? (
              <Card className="p-8 bg-white border-4 border-gray-300">
                <p className="text-gray-600 text-center text-lg">{t('noAdmins')}</p>
              </Card>
            ) : (
              <div className="space-y-4">
                {admins.map((admin) => (
                  <Card key={admin.id} className="p-6 bg-white border-4 border-gray-300 shadow-[4px_4px_0_0_#9ca3af]">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-4">
                          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full border-4 border-black shadow-[2px_2px_0_0_#000] flex items-center justify-center">
                            <span className="text-white font-bold text-lg">
                              {admin.is_root_admin ? '👑' : '👤'}
                            </span>
                          </div>
                          <div>
                            <h3 className="text-lg font-bold text-gray-900">
                              {admin.users?.name || admin.email}
                            </h3>
                            <p className="text-gray-600">{admin.email}</p>
                            <div className="flex items-center space-x-2 mt-1">
                              {admin.is_root_admin && (
                                <span className="bg-yellow-200 border-2 border-yellow-600 rounded-full px-2 py-1 text-xs font-bold text-yellow-800">
                                  {t('rootAdmin')}
                                </span>
                              )}
                              {admin.can_manage_admins && (
                                <span className="bg-blue-200 border-2 border-blue-600 rounded-full px-2 py-1 text-xs font-bold text-blue-800">
                                  Can Manage Admins
                                </span>
                              )}
                              {!admin.is_root_admin && !admin.can_manage_admins && (
                                <span className="bg-gray-200 border-2 border-gray-600 rounded-full px-2 py-1 text-xs font-bold text-gray-800">
                                  {t('regularAdmin')}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      {permissions.isRootAdmin && (
                        <div className="flex items-center space-x-2">
                          {!admin.is_root_admin && (
                            <Button
                              onClick={() => handleTogglePermissions(admin.id, 'is_root_admin', admin.is_root_admin)}
                              variant="brutal-normal"
                              className="text-xs bg-yellow-500 hover:bg-yellow-600"
                            >
                              👑 {t('makeRoot')}
                            </Button>
                          )}
                          
                          <Button
                            onClick={() => handleTogglePermissions(admin.id, 'can_manage_admins', admin.can_manage_admins)}
                            variant="brutal-normal"
                            className="text-xs bg-blue-500 hover:bg-blue-600"
                          >
                            ⚙️ {admin.can_manage_admins ? 'Remove' : 'Add'} Manage
                          </Button>
                          
                          <Button
                            onClick={() => handleRemoveAdmin(admin.id)}
                            variant="brutal-normal"
                            className="text-xs bg-red-500 hover:bg-red-600"
                          >
                            🗑️ {t('removeAdmin')}
                          </Button>
                        </div>
                      )}
                    </div>
                    
                    <div className="mt-4 text-sm text-gray-500">
                      <p>{t('createdAt')}: {new Date(admin.created_at).toLocaleDateString()}</p>
                      {admin.added_by?.users && (
                        <p>{t('addedBy')}: {admin.added_by.users.name || admin.added_by.users.email}</p>
                      )}
                    </div>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
